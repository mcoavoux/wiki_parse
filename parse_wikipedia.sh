
wget https://dumps.wikimedia.org/other/cirrussearch/20171009/frwiki-20171009-cirrussearch-content.json.gz

mkdir -p extracted_texts
# make sure this calls python2
python2 wikiextractor/cirrus-extract.py -o extracted_texts/frwiki frwiki-20171009-cirrussearch-content.json.gz

model=mtg/mind_the_gap_v1.2/pretrained_models_projective/ml_lex/FRENCH/

python3 parse_wiki.py mtg2_parser ${model} nlp-toolbox/tokenizer/ --threads 20


