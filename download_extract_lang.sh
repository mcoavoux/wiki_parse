
date=$1
lang=$2

prefix=https://dumps.wikimedia.org/other/cirrussearch/${date}

suffix=-${date}-cirrussearch-content.json.gz

all="${lang}wikibooks ${lang}wikinews ${lang}wiki ${lang}wikiquote ${lang}wikisource ${lang}wikiversity ${lang}wiktionary ${lang}wikivoyage"

mkdir -p extracted_texts
for wik in ${all}
do
    if [[ `wget -S --spider ${prefix}/${wik}${suffix} 2>&1 | grep 'HTTP/1.1 200 OK'` ]]
    then 
        wget ${prefix}/${wik}${suffix}
        python2 wikiextractor/cirrus-extract.py -o extracted_texts/${wik} ${wik}${suffix}
    fi
done
