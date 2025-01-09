## LLM

- https://github.com/run-llama/llama_index
  - https://python.langchain.com/docs/integrations/llms/ollama/
- [model arch llama - parameters 8.03B - quantization Q4_K_M 4.9GB](https://ollama.com/library/llama3.1)
- [model arch llama - parameters 3.21B - quantization Q4_K_M 2.0GB](https://ollama.com/library/llama3.2)
- [model arch llama - parameters 70.6B - quantization Q4_K_M  43GB](https://ollama.com/library/llama3.3)
- https://ollama.com/library/qwen2.5:32b
- https://ollama.com/library/command-r:35b
- https://ollama.com/library/gemma2:27b
- https://ollama.com/library/phi3:14b
- https://ollama.com/library/phi3.5:3.8b
- https://ollama.com/library/mistral:7b
- https://ollama.com/library/qwen2.5-coder:7b

```sh
uv init
uv add --dev pip
uv add llama-index-llms-ollama

ollama start
# США
## Meta
ollama run llama3.2:1b
ollama run llama3.2:3b
ollama run llama3.1:8b 
ollama run llama3.3:70b
ollama run firefunction-v2:70b # function calling

## Google
ollama run gemma2:2b
ollama run gemma2:9b
ollama run gemma2:27b 

## Microsoft
ollama run phi3.5:3.8b
ollama run phi3:14b

## NVIDIA
ollama run nemotron-mini:4b
ollama run nemotron:70b

## Франция - Mistral
ollama run mistral:7b
ollama run mistral-nemo:12b
ollama run mistral-small:22b

## Канада - Cohere
ollama run command-r:35b

# Китай
## Alibaba
ollama run qwen2.5:0.5b
ollama run qwen2.5:1.5b
ollama run qwen2.5:3b 
ollama run qwen2.5:14b
ollama run qwen2.5:32b
ollama run qwen2.5:72b
ollama run qwq:32b     # reasoning
ollama run marco-o1:7b # reasoning </Thought><Output>

## DeepSeek
ollama run deepseek-v2:16b # Lite-Chat MoE

set m deepseek-v2:16b
ollama show --template $m > d/llm/tpl/$m.tpl

brew install sqlite3_analyzer
sqlite3_analyzer d/llm/llm.db
```

## tables

- https://docs.sqlalchemy.org/en/20/orm/quickstart.html
- https://qna.habr.com/q/1295182
- https://github.com/fastapi/sqlmodel
  - https://chatgpt.com/share/6777e7cf-7af0-800a-8f38-4ce368a12bb3
  - https://chatgpt.com/share/6777e7a5-ae4c-800a-a529-776174d53f36

- corpus  
  - id: 1
  - name: iswoc
- doc
  - id: 1
  - name: forms.txt
  - corpus: 1
- line
  - id: 1
  - doc: 1
- form
  - id: 1
  - line: 1
  - num: 1
  - form: Mæg
  - lemma: mag
- model
  - id: 1
  - name: mistral:7b
- predict
  - id: 1
  - model: 1
  - line: 1
  - done: True
  - no_eq: 9
  - at: 2025-01-03T10:23:28.830015Z
  - load_duration:          21 163 667
  - prompt_eval_duration:  261 000 000
  - eval_duration:         551 000 000
  - prompt_tokens:     30
  - completion_tokens: 31
  - temperature: 0.0
- predict_raw
  - id: 1
  - promt: "\n Perform lemmatization of the following Old English text: ..."
  - content: [{'word_form': ..."
  - forms: "Mæg gehyran ..."
  - lemmas: "mag gehyran ..."
  - tool_calls: null
- llm
  - id: 1
  - predict: 1
  - form: 1
  - lemma: mag
  - eq: True
- llm_raw
  - id: 1
  - en: can
  - ru: может
  - morph: "pronoun, 3rd person singular present subjunctive of magan (can)"
  - syntax: subject
  - raw: {'word_form': 'Mæg', 'lemma': 'mag', 'translation_en': 'can','translation_ru': 'может', 'morph_analysis': 'pronoun, 3rd person singular present subjunctive of magan (can)', 'syntax_analysis': 'subject'}
