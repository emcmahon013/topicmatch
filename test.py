import nltk
import re
import enchant
from nltk import Tree
import string




sents=nltk.sent_tokenize(phrase)
tok_sents=[nltk.word_tokenize(sent) for sent in sents]
tag_sents=[nltk.pos_tag(sent) for sent in tok_sents]
chunk_sents=[nltk.ne_chunk(sent) for sent in tag_sents]
s=""
for sent in chunk_sents:
	for chunk in sent:
		if type(chunk) is tuple:
			if chunk[1]!='NNP' or d.check(chunk[0])==True:
				if s=="" or chunk[0] in string.punctuation:
					s+=chunk[0]
				else:
					s+=" "+chunk[0]
		elif type(chunk) is nltk.Tree:
			for subtree in chunk.subtrees():
					if subtree.label()=='GPE' or subtree.label()=='LOCATION' or subtree.label()=='FACILITY':
						print("DEL "+str(chunk))	
					elif d.check(subtree.pos()[0][0][0])==True and subtree.pos()[0][0][0]!='Latin':
						print(chunk[0][0])
						if s=="" or chunk[0][0] in string.punctuation:
							s+=chunk[0][0]
						else:
							s+=" "+chunk[0][0]					
print(s)






# IN=re.compile(r',+\s+as\s+')
# for doc in chunk_sents:
# 	for rel in nltk.sem.extract('LOC',doc, corpus='ieer'):
# 		print(nltk.sem.show_raw_rtuple(rel))
