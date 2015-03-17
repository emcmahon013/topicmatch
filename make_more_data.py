"""make_lda_data. Compile corpus + dictionary from textfile across all submissions.

Usage:
  make_lda_data <textfile> <datafile>
"""

import string, os, codecs, gensim, save

from docopt import docopt
from nltk.corpus import stopwords
from nltk.stem.snowball import PorterStemmer
from nltk.tree import Tree
from nltk.chunk import ne_chunk
import nltk
import re
import enchant


stemmer = PorterStemmer()
stop=stopwords.words('english')
WordList=['located']
for word in WordList:
    stop.append(stemmer.stem(word))
STOPWORDS = set((stemmer.stem(w) for w in stopwords.words('english')))
d=enchant.Dict("en_US")

# Stopwrods include words <= 2 characters.
def remove_stopwords(words):
#    return words
    return [ w for w in words if w not in STOPWORDS and len(w) >= 2 ]

def transform_word(word):
    # don't stem
    # return word.lower().rstrip(string.punctuation)
    return stemmer.stem(word.lower().strip(string.punctuation))

def remove_NER(text):
    sents=nltk.sent_tokenize(text)
    tok_sents=[nltk.word_tokenize(sent) for sent in sents]
    tag_sents=[nltk.pos_tag(sent) for sent in tok_sents]
    new_tags=[remove_unicode(tag) for tag in tag_sents]
    chunk_sents=[nltk.ne_chunk(sent) for sent in new_tags]
    s=""
    for sent in chunk_sents:
        for chunk in sent:
            if type(chunk)!=nltk.Tree:
                if s=="" or chunk[0] in string.punctuation:
                    s+=chunk[0]
                else:
                    s+=" "+chunk[0]
    return s



def remove_place(text):
    CountryList=['puerto','guam','republic','kingdom','region','latin','north','northern','east','eastern','west','western','south','southern','northwest','northwestern','northeast','northeastern','southwest','southwestern','southeast','southeastern','panhandle','gulf']
    sents=nltk.sent_tokenize(text)
    tok_sents=[nltk.word_tokenize(sent) for sent in sents]
    tag_sents=[nltk.pos_tag(sent) for sent in tok_sents]
    chunk_sents=[nltk.ne_chunk(sent) for sent in tag_sents]
    s=""
    for sent in chunk_sents:
        comma=False
        place=False
        for chunk in sent:
            if type(chunk) is tuple:
                if chunk[1]==',' or chunk[0]=='and' or chunk[0]=='or':
                    comma=True
                elif (chunk[0]=='the' or chunk[0]=='in') and place==True:
                    comma=True
                else:
                    comma=False
                    place=False
                if chunk[1]!='NNP' and d.check(chunk[0])==True and chunk[0].lower() not in CountryList:
                    if s=="" or chunk[0] in string.punctuation:
                        s+=chunk[0]
                    else:
                        s+=" "+chunk[0]
            elif type(chunk) is nltk.Tree:
                for subtree in chunk.subtrees():
                        if subtree.label()=='GPE' or subtree.label()=='LOCATION' or subtree.label()=='GSP' or subtree.pos()[0][0][0].lower() in CountryList:
                            place=True    
                        elif d.check(subtree.pos()[0][0][0])==True:
                            n=len(subtree.pos())
                            for i in range(n):
                                word=subtree.pos()[i][0]
                                if comma!=True or place!=True:
                                    if s=="" or word[0] in string.punctuation:
                                        s+=word[0]
                                    else:
                                        s+=" "+word[0]
                                    comma=False
                                    place=False           
    return s

def remove_unicode(tag_sent):
    tag_tracker=[]
    tag_token=[]
    n=len(tag_sent)
    for i in range(n):
        if tag_sent[i][0]=='&':
            tag_token.append(tag_sent[i])
            tag_tracker.append(i)
        try:
            if (i-tag_tracker[len(tag_tracker)-1]==1) and (tag_sent[i][1]=='#' or tag_sent[i][1]=='CD'):
                tag_token.append(tag_sent[i])
                tag_tracker.append(i)
        except IndexError:
            pass
    new_tags=[t for t in tag_sent if t not in tag_token]
    return new_tags


def transform_text(text,textfile):
    if textfile=='abstract.txt' or textfile=='paper.txt':
        s=remove_place(text)
    elif textfile=='risk.txt':
        s=remove_NER(text)
    words = s.split()
    return remove_stopwords(map(transform_word, words))

def texts_iter(filename):
    for f in sorted(os.listdir('.')):
        if f[0] != '.' and os.path.isdir(f):
            try:
                with codecs.open(f + "/" + filename, "r", "utf-8", "ignore") as a:
                    print ("Submission by "+ str(f))
                    raw_text = a.read()
                    yield (f, raw_text, transform_text(raw_text,filename))
            except IOError:
                print "No file for ", f

if __name__ == "__main__":
    args = docopt(__doc__)

    students, raw_texts, texts = zip(*list(texts_iter(args['<textfile>'])))
    dictionary = gensim.corpora.dictionary.Dictionary(texts)
    unfiltered=dictionary.token2id.keys()
    dictionary.filter_extremes(no_below=5,no_above=.6)
    filtered=dictionary.token2id.keys()
    filtered_out=set(unfiltered)-set(filtered)
    dictionary.compactify()
    corpus = map(dictionary.doc2bow, texts)

    save.save(args['<datafile>'], students=students, texts=texts,
            raw_texts=raw_texts, corpus=corpus, dictionary=dictionary)

