"""lda_predict. Predicts topics given a corpus and trained model.

Usage:
  lda_predict <datafile> [--num_topics=<K>]

Options:
  --num_topics=<K>  Number of topics [default: 50].
"""

import gensim, save, csv, codecs
from docopt import docopt

import numpy as np
import networkx as nx
import pandas as pd
from collections import defaultdict
import csv
import json
import logging, bz2
import string, os, codecs, gensim
import pickle
import re

forward_opts={'num_topics':int}


class topic_gen:
    def __init__(self,d):
        self.students=d['students']
        self.texts=d['texts']
        self.raw_texts=d['raw_texts']
        self.corpus=d['corpus']
        self.dictionary=d['dictionary']
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)

    def lda_gen(self,alpha,num_topics):
        if alpha=='auto':
            lda=gensim.models.LdaModel(self.corpus,id2word=self.dictionary,alpha=alpha,eval_every=5,num_topics=num_topics,eta=.01)
        else:
            lda=gensim.models.LdaModel(self.corpus,id2word=self.dictionary,alpha=alpha,num_topics=num_topics,eta=.01)
        return lda

    def print_topic(self,lda,num_topics):
        for i in range(0,lda.num_topics):
            print("topic "+str(i)+": "+str(lda.print_topic(i)))
        #now priting to file
        cols=["topic"+str(n) for n in range(0,num_topics)]
        cols.append('text')
        topic_list=pd.DataFrame(index=self.students,columns=cols)
        # counter=0
        # for doc in self.corpus:
        #     vector=lda[doc]
        #     for v in vector:
        #         value="topic"+str(v[0])
        #         topic_list.loc[self.students[counter]][value]=float(v[1])
        #         topic_list.loc[self.students[counter]]['text']=self.raw_texts[counter]
        #     # print(topic_list.loc[students[counter]])
        #     counter+=1
        n=len(self.corpus)
        for i in range(n):
            student=str(self.students[i])
            text=self.raw_texts[i]
            vector=lda[self.corpus[i]]
            for v in vector:
                value="topic"+str(v[0])
                topic_list.loc[student][value]=float(v[1])
                topic_list.loc[student]['text']=text
        return topic_list


if __name__ == "__main__":
    args = docopt(__doc__)
    lda_kwargs = dict((k[2:], forward_opts[k[2:]](v))
        for (k, v) in args.iteritems()
            if k[2:] in forward_opts and v)
    print(lda_kwargs)
    K=lda_kwargs['num_topics']
    print("K: "+str(K))
    d = save.load(args['<datafile>'])
    TG=topic_gen(d)
    lda=TG.lda_gen('auto',K)
    topic_list=TG.print_topic(lda,K)
    topic_list.to_csv('/Users/erinmcmahon/mygit/topicmatch/topic_list.csv',sep=',',encoding='ISO-8859-1')
    # lda2=TG.lda_gen(.01,K)
    # topic_list2=TG.print_topic(lda2,K)
    # topic_list2.to_csv('/Users/erinmcmahon/mygit/topicmatch/topic_list2.csv',sep=',',encoding='ISO-8859-1')



