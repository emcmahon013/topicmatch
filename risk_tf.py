"""risk_tf. Predicts topics given a corpus and trained model.

Usage:
  risk_tf <datafile> 

"""
from docopt import docopt
import save
import gensim

if __name__=="__main__":
	args=docopt(__doc__)
	d=save.load(args['<datafile>'])
	corpus=d['corpus']
	dictionary=d['dictionary']
	TfidfModel=gensim.models.tfidfmodel.TfidfModel
	tfidf=TfidfModel(corpus,dictionary=dictionary)
	for doc in tfidf[corpus]:
		print(doc)
