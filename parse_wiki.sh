
wget https://dumps.wikimedia.org/other/cirrussearch/20171009/frwikiquote-20171009-cirrussearch-content.json.gz

git clone https://github.com/attardi/wikiextractor.git

mkdir extracted_texts

cd wikiextractor
python cirrus-extract.py -o ../extracted_texts/frwikiquote ../frwikiquote-20171009-cirrussearch-content.json.gz



git clone https://github.com/mcoavoux/nlp-toolbox.git
cd nlp-toolbox/tokenizer
make
cd ../..

git clone https://github.com/mcoavoux/mtg
cd mtg/mind_the_gap_v1.2/
mkdir bin
cd lib
bash get_dependencies.bash
cd ../src
make clean
make wstring
cd ../../..


