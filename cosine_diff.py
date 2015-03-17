"""cosine_diff. Compute cosine similarity between company and industry.

Usage:
  cosine_diff <datafile>
"""

import string, os, codecs, gensim, save
from docopt import docopt
import csv
import numpy as np
import pandas as pd
from lda_predict import topic_gen
from topics import aggregate,clean_topics

forward_opts={'num_topics':int}

def cos_company(comp_vec,comp_name,comp_ind,company,ind_match):
	max_cos=0
	n=len(company)
	for i in range(n):
		comp=company.loc[i]
		if comp['Industry']!=comp_ind:
			temp=comp.fillna(0)
			temp_name=comp['Industry']
			del temp['Industry']
			del temp['Symbol']
			cos=cos_sim(comp_vec,temp)
			if abs(cos)>max_cos:
				max_cos=abs(cos)
				ind_name=temp_name
	if max_cos>0:
		ind_match[comp_name]=ind_name
	else:
		ind_match[comp_name]=None
	return ind_match


def cos_industry(comp_name,comp_ind,comp_vec,industry,ind,ind_match):
	abs_cos=0
	for j in ind:
		if j!=comp_ind:
			ind_vec=industry.loc[j]
			ind_vec=ind_vec.fillna(0)
			cos=cos_sim(comp_vec,ind_vec)
			if abs(cos)>abs_cos:
				abs_cos=abs(cos)
				ind_min=j
	ind_match[comp_name]=ind_min
	return ind_match	


def cos_sim(comp_vec,ind_vec):
	dot=np.dot(comp_vec,ind_vec)
	l2=np.linalg.norm(comp_vec)*np.linalg.norm(ind_vec)
	cos=dot/l2
	return cos

def ortho_comp(comp_vec,comp_name,comp_ind,company):
	n=len(company)
	for i in range(n):
		comp=company.loc[i]
		if comp['Industry']==comp_ind and comp['Symbol']!=comp_name:
			del comp['Symbol']
			del comp['Industry']
			dot=np.array(comp_vec)-np.array(comp)
			dot=pd.Series(dot)
			dot=dot.fillna(0)
			# ortho=np.cross(np.array(comp_vec),np.array(comp))
			# ortho=pd.Series(dot)
			# ortho=ortho.fillna(0)
	return dot

def ortho_ind(comp_vec,comp_ind,ind,industry):
	for j in ind:
		if j==comp_ind:
			dot=np.array(comp_vec)-np.array(industry.loc[j])
			dot=pd.Series(dot)
			dot=dot.fillna(0)
	return dot



def find_next(company,industry,join):
	ind_match={}
	ind=list(industry.index)
	n=len(company)
	for i in range(n):
		comp_vec=company.loc[i]
		comp_name=comp_vec['Symbol']
		del comp_vec['Symbol']
		comp_ind=comp_vec['Industry']
		del comp_vec['Industry']
		comp_vec=comp_vec.fillna(0)
		if join=='Industry':
			ind_vec=industry.loc[comp_ind]
			ind_vec=ind_vec.fillna(0)
			comp_vec=ortho_ind(comp_vec,comp_ind,ind,industry)
			ind_match=cos_industry(comp_name,comp_ind,comp_vec,industry,ind,ind_match)
		elif join=='Company':
			comp_vec=ortho_comp(comp_vec,comp_name,comp_ind,company)
			ind_match=cos_company(comp_vec,comp_name,comp_ind,company,ind_match)
		print("company: "+str(comp_name)+", old industry: "+str(comp_ind)+", new industry: "+str(ind_match[comp_name]))
	return ind_match

def new_topics(num_topics,comp):
	d = save.load(args['<datafile>'])
	TG=topic_gen(d)
	lda=TG.lda_gen('auto',num_topics)
	topics=TG.print_topic(lda,num_topics)
	topics.to_csv('/Users/erinmcmahon/mygit/topicmatch/topic_list.csv',sep=',',encoding='ISO-8859-1')
	file='/Users/erinmcmahon/mygit/topicmatch/topic_list.csv'
	topics=pd.read_csv(file,encoding='ISO-8859-1')
	industry=aggregate(topics,comp,csv=True,std=False)
	topics=clean_topics(topics,csv=True)
	company=pd.merge(topics,comp[['Symbol','Industry']],on='Symbol')
	return company,industry

def main(comp,topics,join='Industry'):
	company,industry=new_topics(topics,comp)
	ind_match=find_next(company,industry,join)
	return ind_match


if __name__ == "__main__":
    args = docopt(__doc__)
    file='/Users/erinmcmahon/mygit/topicmatch/COMP.csv'
    comp=pd.read_csv(file,encoding='ISO-8859-1')
    ind_match=main(comp,50)
    writer=csv.writer(open('ortho_match2.csv','wb'))
    for key, value in ind_match.items():
    	writer.writerow([key,value])



    ##NEW THOUGHT: TAKE THE MAX OF THE INDUSTRY MEDIAN/MEAN OR SPECIFIC COMPANY.
    ##THEN SUBTRACT.  (ANYTHING <0, SET TO 0)
