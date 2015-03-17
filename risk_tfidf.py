"""risk_tfidf. Compile corpus + dictionary from textfile across all submissions.

Usage:
  risktfidf <textfile>
 """

from docopt import docopt
from nltk.corpus import stopwords
from nltk.stem.snowball import PorterStemmer
import re
import nltk
import os, codecs, string, save 
import enchant

stemmer = PorterStemmer()
stop=stopwords.words('english')
WordList=['may','can','could','item','risk','factor','would','tend']
STOPWORDS = set((stemmer.stem(w) for w in stopwords.words('english')))
d=enchant.Dict("en-US")

def list_to_text(s,word,punctuation):
	if s=="" or word in punctuation:
		s+=word
	else:
		s+=" "+word
	return s

def clean(words):
	stems=[]
	for word in words:
		if word not in STOPWORDS and len(word)>=2:
			if d.check(word)==False:
				if word[0].isupper()==False:
					try:
						token=nltk.word_tokenize(d.suggest(word)[0])
						if len(word)>1:
							stem=clean(token)
							if len(stem)>0:
								stems.extend(stem)
					except IndexError:
						pass
			else:
				stem=stemmer.stem(word.lower().strip(string.punctuation))
				stems.append(stem)
		else:
			pass
	return stems

def remove_unicode(text, punctuation):
	for s in punctuation:
		text=text.replace(s," ")
	return text
    # tag_tracker=[]
    # tag_token=[]
    # n=len(tag_sent)
    # for i in range(n):
    #     if tag_sent[i][0]=='&':
    #         tag_token.append(tag_sent[i])
    #         tag_tracker.append(i)
    #     try:
    #         if (i-tag_tracker[len(tag_tracker)-1]==1) and (tag_sent[i][1]=='#' or tag_sent[i][1]=='CD'):
    #             tag_token.append(tag_sent[i])
    #             tag_tracker.append(i)
    #     except IndexError:
    #         pass
    # new_tags=[t for t in tag_sent if t not in tag_token]
    # return new_tags

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

def remove_unis(text):
    sents=nltk.sent_tokenize(text)
    tok_sents=[nltk.word_tokenize(sent) for sent in sents]
    tag_sents=[nltk.pos_tag(sent) for sent in tok_sents]
    new_tags=[remove_unicode(tag) for tag in tag_sents]
    s=""
    for sent in new_tags:
    	for chunk in sent:
    		s=list_to_text(s,chunk[0],string.punctuation)
    return s	

def transform_text(text):
	punctuation=string.punctuation
	for d in string.digits:
		punctuation=punctuation+str(d)
	s=remove_unicode(text,punctuation)
	words=s.split()
	# print(words)
	stems=clean(words)
	s=""
	for word in stems:
		s=list_to_text(s,word,string.punctuation)
	return s


def texts_iter(filename):
    for f in sorted(os.listdir('.')):
        if f[0] != '.' and os.path.isdir(f):
            try:
                with codecs.open(f + "/" + filename, "r", "utf-8", "ignore") as a:
                    print ("Submission by "+ str(f))
                    raw_text = a.read()
                    print(transform_text(raw_text))
                    yield(f, raw_text, transform_text(raw_text))
            except IOError:
                print "No file for ", f

if __name__=="__main__":
	args=docopt(__doc__)
	company,raw_texts,texts=zip(*list(texts_iter(args['<textfile>'])))
	X=np.array([' '.join(el) for el in texts])
	vectorizer=TfidfVectorizer(min_df=5,max_df=.95,ngram_range=(1,3),stopwords='english',strip_accents='unicode')
	vectorizer.build_prepocessor()






