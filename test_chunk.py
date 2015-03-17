import string, os, codecs, gensim, save

from docopt import docopt
from nltk.corpus import stopwords
from nltk.stem.snowball import EnglishStemmer
from nltk.tree import Tree
from nltk.chunk import ne_chunk
import nltk
import re
import enchant


def remove_NER(text):
    sents=nltk.sent_tokenize(text)
    tok_sents=[nltk.word_tokenize(sent) for sent in sents]
    tag_sents=[nltk.pos_tag(sent) for sent in tok_sents]
    chunk_sents=[nltk.ne_chunk(sent) for sent in tag_sents]
    s=""
    for sent in chunk_sents:
        for chunk in sent:
            if type(chunk)!=nltk.Tree:
                if s=="" or chunk[0] in string.punctuation:
                    s+=chunk[0]
                else:
                    s+=" "+chunk[0]
    return s

