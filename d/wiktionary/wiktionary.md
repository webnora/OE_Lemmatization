# wiktionary

- https://en.wiktionary.org/wiki/Category:Old_English_lemmas
- https://github.com/unimorph/wiktionary-tools

```sh
uv add zimply pandas
set p s/wiktionary-tools
# set d d/wiktionary/zim/wiktionary_ang_all_maxi_2024-06.zim
set w d/wiktionary
set d $w/zim/wiktionary_en_all_nopic_2024-05.zim
set l $w/lang.txt
uv run $p/zim_extract_lemmaList.py -zimfile $d -langfile $l # 1.5m
uv run $p/zim_extract_all.py -zimfile $d -langfile $l # 1.4m
uv run $p/extract_example_tables.py -candidates_dir $w/zim/candidate_pages # 7.5s empty :(

# uv run $p/zim_extract_lemmaList.py -zimfile $d -langfile $p/languages.txt
cd d/wiktionary/zim/ &&\
  wget -c https://download.kiwix.org/zim/wiktionary/wiktionary_en_all_nopic_2024-05.zim
```
