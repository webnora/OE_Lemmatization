## uv

- https://docs.astral.sh/uv/getting-started/features/

```sh
brew install uv
uv run --with jupyter jupyter lab

uv init
uv venv --seed
uv run Lemmatizer.py > d/Lemmatizer/stat.txt
uv run corpus.py > d/corpus/stat.txt
```

## git submodule

```sh
git submodule add --name syntacticus-treebank-data --depth 1 https://github.com/syntacticus/syntacticus-treebank-data s/syntacticus-treebank-data
git submodule add --name ang_models_cltk https://github.com/cltk/ang_models_cltk s/ang_models_cltk
git submodule add --name wiktionary-tools https://github.com/unimorph/wiktionary-tools s/wiktionary-tools 
git submodule add --name nora_cltk -- git@github.com:webnora/oe_cltk.git s/oe_cltk
git submodule add --name nora_data -- git@github.com:webnora/OE_data.git s/oe_data
```
