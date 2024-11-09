# wiktionary

- https://en.wiktionary.org/wiki/Category:Old_English_lemmas
- https://github.com/unimorph/wiktionary-tools

```sh
uv add zimply pandas
set p s/wiktionary-tools
set d d/wiktionary/zim/wiktionary_en_all_nopic_2024-05.zim
uv run $p/zim_extract_lemmaList.py -zimfile $d -langfile $p/languages.txt
cd d/wiktionary/zim/ &&\
  wget -c https://download.kiwix.org/zim/wiktionary/wiktionary_en_all_nopic_2024-05.zim
```
