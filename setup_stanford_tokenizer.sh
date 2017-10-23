

if [ ! -e stanford-parser.jar ]
then
    if [ ! -e stanford-parser-full-2016-10-31.zip ]
    then
        wget http://nlp.stanford.edu/software/stanford-parser-full-2016-10-31.zip
    fi
    unzip stanford-parser-full-2016-10-31.zip -d .
    cp stanford-parser-full-2016-10-31/stanford-parser.jar .
    rm -r stanford-parser-full-2016-10-31
fi
