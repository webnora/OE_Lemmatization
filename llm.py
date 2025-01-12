import os
from llama_index.llms.ollama import Ollama
import json
from dataclasses import dataclass, astuple, fields
from db import DB, Corpus, Doc, Line, Form, Predict, PredictRaw, Lemma, LemmaRaw
from pandas import DataFrame as df
from datetime import datetime
from textwrap import dedent, wrap
import re

@dataclass
class Model:
  llama_1b   : str = "llama3.2:1b"
  llama_3b   : str = "llama3.2:3b"
  llama_8b   : str = "llama3.1:8b"
  llama_70b  : str = "llama3.3:10b"
  mistral_7b : str = "mistral:7b"
  mistral_12b: str = "mistral-nemo:12b"
  mistral_22b: str = "mistral-small:22b"

class LLM:
  temperature = 0.0
  request_timeout = 3600.0
  query = "Сколько букв в слове привет? Выведи каждую букву отдельно."
  text = (
    'Mæg gehyran'
    # 'Apollonius cweþan'
    # 'Mæg gehyran se ðe wyle be þam halgan mædene Eugenian Philyppus dæhter hu heo ðurh mægðhad mærlice þeah and þurh martyrdom þisne middaneard oferswað\n'
    # 'Sum æþelboren þægn wæs Philippus gehaten ðone asende se casere Commodus þe on ðam dagum rixode fram Rome.byrig to ðære byrig ðe is gehaten Alexandria'
  )
  path_example = 'd/llm/examples'

  def __init__(self, path=path_example, **kwargs):
    defaults = {
        "model": Model.mistral_7b,
        "temperature": 0.0,
        "request_timeout": 3600.0
    }
    self.llm = Ollama(**{**defaults, **kwargs})
    self.path = f'{path}/{self.llm.model}'
    if not os.path.exists(self.path):
      os.makedirs(self.path)
    self.db = DB()
    self.json_array = re.compile(r'\[\s*\{.*?\}\s*\]', re.DOTALL)

  def log(self, line_id = ''):
    with open(f'{self.path}/raw{line_id}.json', 'w') as f:
      f.write(self.response.model_dump_json(indent=2))

  def log_json(self, line_id = ''):
    with open(f'{self.path}/data{line_id}.json', 'w') as f:
      json.dump(self.json, f, indent=2, ensure_ascii=False)

  def log_err(self, line_id = ''):
    with open(f'{self.path}/err{line_id}.json', 'w') as f:
      f.write(self.response.text)

  def complete(self, query=query):
    r = self.llm.complete(query)
    self.response = r
    if r:
      self.log()
      return r.text
    print(f'ERR: {r}')

  def complete_json(self, text=text):
    content = self.complete(text)
    if content:
      match = self.json_array.search(content)
      if not match:
        print(f"json array search ERR: {content[:100]}")
      json_array = match.group()
      try:
        self.json = json.loads(json_array)
      except Exception as e:
        self.log_err()
        print(f"json load ERR: {json_array[:100]}")
        return 
      self.log_json()
      return json_array
    print('ERR: lemmatize')

  def debug(self):
    print(self.response.text)
    print()
    print(self.response.raw)

  def promt_v1(self, text=text):
    return dedent(f"""
      Perform lemmatization of the following Old English text:
      {text}

      Return the result as a JSON array where each item contains:
      - word_form: the original word form
      - lemma: the lemma of the word
      - translation_en: the English translation of the lemma
      - translation_ru: the Russian translation of the lemma
      - morph_analysis: morphological analysis
      - syntax_analysis: syntactic analysis
      The result should be just json without formatting and text descriptions.
    """).strip()

  def lemmatize(self, line=None, test = False):
    if not line:
      line = self.db.get_test_line()
      test = True
    promt = self.promt_v1(line.line)
    try:
      content = self.complete_json(promt)
    except Exception as e:
      return f"line: {line.id} ERR: {str(e)[:100]}"
    if not content:
      return f"line: {line.id} ERR: not content"
    json = self.json
    model = self.llm
    raw = self.response.raw
    prediction = Predict(
      line_id = line.id, # line = line,
      test = test,
      model = model.model,
      temperature = model.temperature, 
      done = raw["done"], 
      at = datetime.fromisoformat(raw["created_at"]),
      **{k:raw[k] for k in ["load_duration", "prompt_eval_duration", "eval_duration"]},
      **{k:raw["usage"][k] for k in ["prompt_tokens", "completion_tokens"]},
      no_eq = 0,
      raw=PredictRaw(promt=promt, content=content), # type: ignore
    )
    if len(json) < len(line.forms):
      return f"line: {line.id} ERR: {len(json)} < {len(line.forms)}"
    for form in line.forms:
      d = json[form.num]
      if form.form != d["word_form"]:
        print(f"line: {line.id} ERR: {form} != {d}")
        return 
      lemma = d["lemma"]
      eq = (form.lemma == lemma)
      prediction.no_eq += int(not eq)
      prediction.lemmas.append(Lemma(form=form, lemma=lemma, eq=eq,
        raw=LemmaRaw(raw=d, en=d["translation_en"], ru=d["translation_ru"], morph=d["morph_analysis"], syntax=d["syntax_analysis"])
      ))
    self.db.s.add(prediction)
    self.db.s.commit()
    return line.id, prediction.no_eq, len(line.forms)

class LLM_Stream(LLM):
  def stream_complete(self, query = LLM.query):
    stream = self.llm.stream_complete(query)
    for response in stream:
      print(response.delta, end="")
    self.response = response
    self.log()
    return response

if __name__ == "__main__":
  def test_llm_stream():
    llm_stream = LLM_Stream()
    llm_stream.stream_complete("Напиши короткое стихотворение")
    llm_stream.debug()
  def test_llm():
    llm = LLM()
    # llm.complete()
    # llm.debug()
    print(llm.lemmatize())
    # print(llm.promt_v1())
  def test_model():
    print(astuple(Model()))
    print([f.default for f in fields(Model)])
  # test_llm_stream()
  test_llm()
