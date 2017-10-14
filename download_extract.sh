
date=20171009

prefix=https://dumps.wikimedia.org/other/cirrussearch/${date}

suffix=-${date}-cirrussearch-content.json.gz

all="frwikibooks frwikinews frwiki frwikiquote frwikisource frwikiversity frwikivoyage frwiktionary"

mkdir -p extracted_texts
for wik in ${all}
do
    wget ${prefix}/${wik}${suffix}
    python2 wikiextractor/cirrus-extract.py -o extracted_texts/${wik} ${wik}${suffix}
done


