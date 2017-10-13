

prefix=https://dumps.wikimedia.org/other/cirrussearch/20171009

date=20171009
suffix=-${date}-cirrussearch-content.json.gz

all=frwikibooks frwikinews frwiki frwikiquote frwikisource frwikiversity frwikivoyage frwiktionary

mkdir -p extracted_texts
for wik in ${all}
do
    wget ${prefix}/${wik}${suffix}
    python2 wikiextractor/cirrus-extract.py -o extracted_texts/${wik} ${wik}${suffix}
done


