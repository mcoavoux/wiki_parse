
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


# Setup

Instructions for downloading and compiling these tools are in `setup.sh`.
To run it, you need boost, g++ and clang++.

# Data

The scripts need cirrus dumps as input, found at [https://dumps.wikimedia.org/other/cirrussearch/](https://dumps.wikimedia.org/other/cirrussearch/).

To download and extract the data for a specific language, run:

    bash download_extract_lang.sh <date> <language code>

where `date` is the time stamp for a wikipedia dump (see what is available
[here](https://dumps.wikimedia.org/other/cirrussearch/))
and language code is the identifier used by wikipedia for the language.


For example:

    bash download_extract_lang.sh 20171009 fr # download French wikis
    bash download_extract_lang.sh 20171009 ko # download Korean wikis


# Parse

Use the script `parse_wiki.py` to parse the data.

    python3 parse_wiki.py --help
    # python3 parse_wiki.py <parser exe> <parsing model> <path to tokenizer> <wiki root>--threads <num of threads> --beam <size of beam>
    
    python3 parse_wiki.py ./mtg2_parser FRENCH ./tokenizer_fr extracted_texts/frwiki --threads 20
    # or
    python3 parse_wiki.py "./mtg2_parser -p " FRENCH ./tokenizer_fr extracted_texts/frwiki --threads 20

The `-p` option precomputes and caches character-based word embeddings
(higher initialization time but faster parsing).


For French, each thread should take less than 1 Go of memory.

Pipeline:

1. Print each article in `<ID>.txt`, where ID is an identifier for the
  article (ex: `https://fr.wikisource.org/?curid=1026462` yields
  the wikisource page for *Du côté de chez Swann*).
2. Call the tokenizer (sentence segmentation, tokenization) and do
  some preprocessing to match the input format of the parser
  (essentially, replace parentheses by `-LRB-` / `-RRB-`).
  This outputs `<ID>.txt.tok` for each `<ID>.txt` file.
3. Call the parser. The parser outputs:
    - `<ID>.txt.conll`: a conll file containing labelled dependency trees
      and morphological analyses.
    - `<ID>.txt.discbracket`: a [discbracket](http://discodop.readthedocs.io/en/latest/fileformats.html#discbracket)
      file containing a constituency tree.





