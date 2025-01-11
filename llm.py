import os
from llama_index.llms.ollama import Ollama
import json
from dataclasses import dataclass, astuple, fields
from db import DB, Corpus, Doc, Line, Form, Predict, Lemma, LemmaRaw
from pandas import DataFrame as df

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

  def log(self):
    with open(f'{self.path}/raw.json', 'w') as f:
      f.write(self.response.model_dump_json(indent=2))

  def log_json(self):
    with open(f'{self.path}/data.json', 'w') as f:
      json.dump(self.json, f, indent=2, ensure_ascii=False)

  def complete(self, query=query):
    self.response = self.llm.complete(query)
    self.log()
    return self.response

  def debug(self):
    print(self.response.text)
    print()
    print(self.response.raw)

  def lemmatize(self, text=text):
    prompt = f"""
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
    """
    self.json = json.loads(self.complete(prompt).text)
    self.log_json()
    return self.json

  def lemmatize_test(self):
    line = self.db.get_test_line()
    json = self.lemmatize()
    return json

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
    print(llm.lemmatize_old_english())
  def test_model():
    print(astuple(Model()))
    print([f.default for f in fields(Model)])
  # test_llm_stream()
  test_llm()
