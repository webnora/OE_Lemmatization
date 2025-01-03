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
- https://ollama.com/library/mistral:7b

```sh
uv init
uv add --dev pip
uv add llama-index-llms-ollama

ollama start
# США
# Meta
ollama run llama3.2:1b
ollama run llama3.2:3b
ollama run llama3.1:8b 
ollama run llama3.3:70b

# Google
# ollama run gemma2:2b
# ollama run gemma2:9b
ollama run gemma2:27b 

# Microsoft
# ollama run phi3.5:3.8b
ollama run phi3:14b

## Канада - Cohere
ollama run command-r:35b

## Китай - Alibaba
# ollama run qwen2.5:0.5b
# ollama run qwen2.5:1.5b
ollama run qwen2.5:3b 
ollama run qwen2.5:14b
ollama run qwen2.5:32b
ollama run qwen2.5:72b

## Франция - Mistral
ollama run mistral:7b
ollama run mistral-nemo:12b
ollama run mistral-small:22b
```
