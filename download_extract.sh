

prefix=https://dumps.wikimedia.org/other/cirrussearch/20171009/


wikibooks=frwikibooks-20171009-cirrussearch-content.json.gz
wikinews=frwikinews-20171009-cirrussearch-content.json.gz
wiki=frwiki-20171009-cirrussearch-content.json.gz
wikiquote=frwikiquote-20171009-cirrussearch-content.json.gz
wikiversity=frwikiversity-20171009-cirrussearch-content.json.gz
wikivoyage=frwikivoyage-20171009-cirrussearch-content.json.gz
wiktionary=frwiktionary-20171009-cirrussearch-content.json.gz


wget ${prefix}/${wikibooks}
wget ${prefix}/${wikinews}
#wget ${prefix}/${wiki}
wget ${prefix}/${wikiquote}
wget ${prefix}/${wikisource}
wget ${prefix}/${wikiversity}
wget ${prefix}/${wikivoyage}
wget ${prefix}/${wiktionary}

mkdir -p extracted_texts

python2 wikiextractor/cirrus-extract.py -o extracted_texts/wikibooks ${wikibooks}
python2 wikiextractor/cirrus-extract.py -o extracted_texts/wikinews ${wikinews}
#python2 wikiextractor/cirrus-extract.py -o extracted_texts/wiki ${wiki}
python2 wikiextractor/cirrus-extract.py -o extracted_texts/wikiquote ${wikiquote}
python2 wikiextractor/cirrus-extract.py -o extracted_texts/wikisource ${wikisource}
python2 wikiextractor/cirrus-extract.py -o extracted_texts/wikiversity ${wikiversity}
python2 wikiextractor/cirrus-extract.py -o extracted_texts/wikivoyage ${wikivoyage}
python2 wikiextractor/cirrus-extract.py -o extracted_texts/wiktionary ${wiktionary}
