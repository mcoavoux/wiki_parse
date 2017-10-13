

## setup up necessary tools


# Download wikiextractor
git clone https://github.com/attardi/wikiextractor.git


# Download and compile tokenizer for French:
git clone https://github.com/mcoavoux/nlp-toolbox.git
cd nlp-toolbox/tokenizer
make clean
make
cd ../..


# Download and compile parser
git clone https://github.com/mcoavoux/mtg.git
cd mtg/mind_the_gap_v1.2/
mkdir bin
cd lib
bash get_dependencies.bash
cd ../src
make clean
make wstring
cd ../../..
cp mtg/mind_the_gap_v1.2/bin/mtg2_parser .


