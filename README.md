
# Parsing Wikipedia

This repository contains scripts for parsing wikipedia (and other wikis)
easily. It initially aims at parsing French-language wikis, but
will be extended to other languages.

It is based on the following tools:

- [mtg parser](https://github.com/mcoavoux/mtg/): outputs constituency
    trees, labelled dependency trees and morphological analyses.
- Benoît Crabbé's [tokenizer](https://github.com/bencrabbe/nlp-toolbox/),
    [forked version](https://github.com/mcoavoux/nlp-toolbox/)
- Giuseppe Attardi's [wikiextractor](https://github.com/attardi/wikiextractor)


# Set up

Instructions for downloading and compiling these tools are in `setup.sh`.
To run it, you need boost, g++ and clang++.

# Data

The scripts need cirrus dumps as input, found at:

    https://dumps.wikimedia.org/other/cirrussearch/
    
    # Example: french wikiquote
    wget https://dumps.wikimedia.org/other/cirrussearch/20171009/frwikiquote-20171009-cirrussearch-content.json.gz

Preprocess the data with `wikiextractor`:

    mkdir -p extracted_texts
    python2 wikiextractor/cirrus-extract.py -o extracted_texts/frwikiquote frwikiquote-20171009-cirrussearch-content.json.gz

Make sure the python command you use call Python2.


# Parse

Use the script `parse_wiki.py` to parse the data.

    python3 parse_wiki.py --help
    python3 parse_wiki.py mtg2_parser mtg/mind_the_gap_v1.2/pretrained_models_projective/ml_lex/FRENCH/ nlp-toolbox/tokenizer/ --threads 20
    # python3 parse_wiki.py <parser exe> <parsing model> <path to tokenizer root dir> --threads <num of threads> --beam <size of beam>


Pipeline:

1. Print each article in `<ID>.txt`, where ID is an identifier for the
  article (`https://fr.wikipedia.org/?curid=ID` for a wikipedia article).
2. Call the tokenizer (sentence segmentation, tokenization) and do
  some preprocessing to match the input format of the parser
  (essentially, replace parentheses by `-LRB-` / `-RRB-`).
  This outputs `<ID>.txt.tok` for each `<ID>.txt` file.
3. Call the parser. The parser outputs:
    - `<ID>.txt.conll`: a conll file containing labelled dependency trees
      and morphological analyses.
    - `<ID>.txt.discbracket`: a [discbracket](http://discodop.readthedocs.io/en/latest/fileformats.html#discbracket)
      file containing a constituency tree.





