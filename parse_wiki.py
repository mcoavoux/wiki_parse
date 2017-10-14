#encoding:utf8
import os
import os.path
import bz2
import sys
import argparse
from joblib import Parallel, delayed


def get_files(path):
    sys.stderr.write("Entering {}\n".format(path))
    dirs = []
    files = []
    for f in os.listdir(path):
        f = os.path.join(path,f)
        if os.path.isfile(f):
            if all([not f.endswith(end) for end in [".txt", ".conll", ".discbracket", ".tok"]]):
                files.append(f)
        if os.path.isdir(f):
            dirs.append(f)

    for d in dirs:
        files.extend( get_files(d) )

    return files

def normalize_punct(line):
    """
    Adds a dot to lines not ending with strong punctuation
    """
    line = line.strip()
    if line[-1] not in '!?.':
        return line + '.\n'
    return line + "\n"


def extract_doc_index(xmlline):

    for tok in xmlline.split():
        if tok[:2]== "id":
            idx = str(tok).split('=')[1]
            return idx[1:-1]
    return "-1" #error case

def preprocess_file(input_filename):
    dname = os.path.dirname(input_filename)
    instream = open(input_filename, "r")
    idx = None
    ostream = None
    filenames = []
    for line in instream:
        if line.startswith('<doc'):
            idx = extract_doc_index(line)
            outfilename = os.path.join(dname, idx+'.txt')
            ostream = open(outfilename,'w')
            filenames.append(outfilename)
        elif line.startswith('</doc>'):
            ostream.flush()
            ostream.close()
            ostream = None
        elif ostream != None:
            line = line.strip()
            if line:
                ostream.write(normalize_punct(line))
    instream.close()

    if ostream is not None:
        ostream.flush()
        ostream.close()
    
    return filenames


def preprocess_files(input_filenames):
    return [ preprocess_file(filename) for filename in input_filenames ]

def generate_files_bunch(files_list_list):
    tmp = []
    i = 0
    for flist in files_list_list:
        for f in flist:
            tmp.append(f)
            i += 1
            if i % 200 == 0 :
                yield tmp
                tmp = []
    if len(tmp) > 0:
        yield tmp

def do_files(input_filenames, parser_path, parsing_model, tokenizer_path, beamsize, threads):
    
    #files_list_list = preprocess_files(input_filenames)
    files_list_list = Parallel(n_jobs=threads)(delayed(preprocess_file)(filename) for filename in input_filenames)
    sys.stderr.write("Length of bunch of files: {} \n".format([len(l) for l in files_list_list]))
    Parallel(n_jobs=threads)(delayed(nlp_pipeline)(flist, parser_path, parsing_model, tokenizer_path, beamsize) for flist in generate_files_bunch(files_list_list))




def main(parser_path, parsing_model, tokenizer_path, beamsize, threads, wiki_root):
    
    file_list = get_files(wiki_root)
    do_files(file_list, parser_path, parsing_model, tokenizer_path, beamsize, threads)
    


def nlp_pipeline(input_filenames, parser_path, parsing_model, tokenizer_path, beamsize):

    #tokenizer_call = "{tokenizer} -p -s -S {cpd}  -P {pref} {infiles}".format(
            #tokenizer = "{}/tokenizer".format(tokenizer_path),
            #cpd = "{}/{}".format(tokenizer_path, "strong-cpd.dic"),
            #pref = "{}/{}".format(tokenizer_path, "prefixes.dic"),
            #infiles = " ".join(input_filenames))

    tokenizer_call = "{tokenizer} {infiles}".format(
            tokenizer = tokenizer_path,
            infiles = " ".join(input_filenames))


    #sys.stderr.write("{}\n".format(tokenizer_call))
    os.system(tokenizer_call)

    assert([input_file.endswith(".txt") for input_file in input_filenames])
    
    tokenized_filenames = [input_file + ".tok" for input_file in input_filenames]
    
    for input_filename,in_file in zip(input_filenames, tokenized_filenames):
        tfile = open(in_file, "r")
    
        out = [line.strip().replace("(", "-LRB-").replace(")", "-RRB-") for line in tfile]
        out = [line for line in out if line]
        tfile.close()
        
        tfile = open(in_file, "w")
        tfile.write("\n".join(out))
        tfile.close()

    parser_call = "{parser} -m {model} -b {beam} {infiles}".format(
            parser = parser_path,
            model = parsing_model,
            beam = beamsize,
            infiles = " ".join(tokenized_filenames))
    
    #sys.stderr.write("{}\n".format(parser_call))
    os.system(parser_call)







if __name__ == "__main__":
    
    usage = """
    Glue scripts together to parse Wik*: wikipedia, wikisource, wikinews, etc.
    
    This script is based on a prior script by Benoît Crabbé.
    
    Dependencies:
    
    - mtg parser -> github.com/mcoavoux/mtg
    - french tokenizer -> github.com/bencrabbe/nlp-toolbox/tokenizer
    
    Input:
    
    - files preprocessed by Giuseppe Attardi's wikiextractor -> https://github.com/attardi/wikiextractor
    
    
    """
    parser = argparse.ArgumentParser(description = usage, formatter_class=argparse.RawTextHelpFormatter)
    
    parser.add_argument("parser", type = str, help="Path to parser executable.")
    parser.add_argument("model", type = str, help="Path to parsing model.")
    parser.add_argument("tokenizer", type=str, help="Path to tokenizer executable.")
    parser.add_argument("wikiroot", type=str, help="Path to the root of the wiki folder.")
    parser.add_argument("--beam", "-b", type=int, help="Beam size [default=1]", default=1)
    parser.add_argument("--threads", "-t", type=int, help="Number of threads [default=1]", default=2)
    

    args = parser.parse_args()
    
    
    main(args.parser, args.model, args.tokenizer, args.beam, args.threads, args.wikiroot)


