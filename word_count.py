#encoding:utf8
import os
import os.path
import bz2
import sys
import argparse
from joblib import Parallel, delayed

from collections import defaultdict


ID, FORM, LEMMA, CPOS, FPOS, MORPH, HEAD, REL, PHEAD, PREL=range(10)

def get_conll_files(path):
    sys.stderr.write("Entering {}\n".format(path))
    dirs = []
    files = []
    for f in os.listdir(path):
        f = os.path.join(path,f)
        if os.path.isfile(f):
            if f.endswith(".conll"):
                files.append(f)
        if os.path.isdir(f):
            dirs.append(f)

    for d in dirs:
        files.extend( get_conll_files(d) )

    return files

def read_conll(filename):
    with open(filename) as f:
        corpus = []
        sentences = f.read().split("\n\n")
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                tokens = [ line.strip().split("\t") for line in sentence.split("\n") ]
                assert(all([len(line) == 10 for line in tokens]))
                corpus.append(tokens)
        return corpus

def write_conll(corpus, filename):
    of = open(filename, "w")
    for sent in corpus:
        for token in sent:
            of.write("{}\n".format("\t".join(token)))
        of.write("\n")
    of.close()

def dump_distribution_dict(filename, dic):
    ofstream = open(filename, "w")
    for item in sorted(dic, key = lambda x : dic[x], reverse = True):
        ofstream.write("{}\t{}\n".format(item, dic[item]))
    ofstream.close()
    
def main(root, output):
    
    os.system("mkdir -p {}".format(output))
    file_list = get_conll_files(root)
    
    
    voc = defaultdict(int)
    tags = defaultdict(int)
    sent_length = defaultdict(int)
    doc_length_s = defaultdict(int)
    doc_length_t = defaultdict(int)
    
    n_tokens = 0
    n_sentences = 0
    n_documents = 0
    
    
    for f in file_list:
        
        corpus = read_conll(f)
        
        n_documents += 1
        doc_length_s[len(corpus)] += 1
        doc_length_t[sum([len(s) for s in corpus])] += 1
        n_sentences += len(corpus)

        for sentence in corpus:
            n_tokens += len(sentence)
            sent_length[len(sentence)] += 1
            for token in sentence:
                voc[token[FORM]] += 1
                tags[token[CPOS]] += 1

    print("Number of documents : {}".format(n_documents))
    print("Number of sentences : {}".format(n_sentences))
    print("Number of tokens : {} (ignoring punctuation: {})".format(n_tokens, n_tokens - tags["PONCT"]))
    print("Number of word types", len(voc))

    dump_distribution_dict(output+"/vocabulary", voc)
    dump_distribution_dict(output+"/tags", tags)
    dump_distribution_dict(output+"/doc_length_w", doc_length_t)
    dump_distribution_dict(output+"/doc_length_s", doc_length_s)
    dump_distribution_dict(output+"/sent_length", sent_length)






if __name__ == "__main__":
    
    usage = """
    Computes some statistics about parsed corpus (number of tokens, word types, etc.):
    
    - Number of documents
        - size of documents (num tokens, num sentences)
    - Number of sentences
        - size of sentences (num tokens)
    - Number of tokens
    - Number of word types (all, excluding NPP and ET)
    """
    
    parser = argparse.ArgumentParser(description = usage, formatter_class=argparse.RawTextHelpFormatter)
    
    parser.add_argument("root", type = str, help="Directory (every subfolder will be searched for conll files)")
    parser.add_argument("output", type = str, help="Output dir")
    
    args = parser.parse_args()
    
    main(args.root, args.output)


