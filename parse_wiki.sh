
wget https://dumps.wikimedia.org/other/cirrussearch/20171009/frwikiquote-20171009-cirrussearch-content.json.gz

mkdir -p extracted_texts

# make sure this calls python2
python2 wikiextractor/cirrus-extract.py -o extracted_texts/frwikiquote frwikiquote-20171009-cirrussearch-content.json.gz


python3 parse_wiki.py mtg/mind_the_gap_v1.2/bin/mtg2_parser mtg/mind_the_gap_v1.2/pretrained_models_projective/ml_lex/FRENCH/ nlp-toolbox/tokenizer/ --threads 20


