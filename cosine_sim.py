"""cosine_sim. Compute cosine similarity between company and industry.

Usage:
  cosine_sim <datafile>
"""

import string, os, codecs, gensim, save
from docopt import docopt

import numpy as np
import pandas as pd
from lda_predict import topic_gen
from topics import aggregate,clean_topics


def cos_sim(comp_vec,ind_vec):
	dot=np.dot(comp_vec,ind_vec)
	l2=np.linalg.norm(comp_vec)*np.linalg.norm(ind_vec)
	cos=dot/l2
	return cos

def industry_matching(comp_name,comp_vec,industry,ind,real_cos,ind_match):
	max_cos=0
	for j in ind:
		ind_vec=industry.loc[j]
		ind_vec=ind_vec.fillna(0)
		cos=cos_sim(comp_vec,ind_vec)
		if cos>max_cos:
			max_cos=cos
			ind_name=j
	if max_cos>real_cos:
		match=False
		dif=max_cos-real_cos
	else:
		match=True
		dif=0
	ind_match[comp_name]=[ind_name,match,dif]
	return ind_match


def sum_cos(company,industry,num_topics):
	cosine_sum=0
	ind_match={}
	matching=0
	ind=list(industry.index)
	cos_ind=dict((key,[0,0]) for key in ind)
	n=len(company)
	for i in range(n):
		comp_vec=company.loc[i]
		comp_name=comp_vec['Symbol']
		del comp_vec['Symbol']
		comp_ind=comp_vec['Industry']
		del comp_vec['Industry']
		ind_vec=industry.loc[comp_ind]
		comp_vec=comp_vec.fillna(0)
		ind_vec=ind_vec.fillna(0)
		cos=cos_sim(comp_vec,ind_vec)
		cosine_sum+=cos
		temp_cos=cos_ind[comp_ind][0]
		temp_no=cos_ind[comp_ind][1]
		cos_ind[comp_ind]=[(temp_cos+cos),temp_no+1]
		ind_match=industry_matching(comp_name,comp_vec,industry,ind,cos,ind_match)
		if ind_match[comp_name][1]==True:
			matching+=1
	return cosine_sum,cos_ind,matching

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

def divide_zero(num,dem):
	if dem==0:
		ans=0
	else:
		ans=num/dem
	return ans

def find_cos(cos_ind):
	cosine_industry=0
	for key in cos_ind:
		cosine_industry+=divide_zero(cos_ind[key][0],cos_ind[key][1])
	return cosine_industry

def topic_compare(comp,topics_min,topics_max,jump=5):
	num_topics=list(range(topics_min,topics_max+1,jump))
	accuracy=pd.DataFrame(index=num_topics,columns=['Total','Industry','Match'])
	for i in num_topics:
		company, industry=new_topics(i,comp)
		# print("COMPANY:" +str(company))
		# print("INDUSTRY: "+str(industry))
		cosine_sum,cos_ind,matching=sum_cos(company,industry,i)
		print(matching)
		cosine_industry=find_cos(cos_ind)
		accuracy.loc[i]['Total']=divide_zero(cosine_sum,len(company))
		accuracy.loc[i]['Industry']=divide_zero(cosine_industry,len(cos_ind))
		accuracy.loc[i]['Match']=float(matching)/float(len(company))
		print("finished round: "+str(i))
		print(accuracy)
	return accuracy



if __name__ == "__main__":
	args = docopt(__doc__)
	file='/Users/erinmcmahon/mygit/topicmatch/COMP.csv'
	comp=pd.read_csv(file,encoding='ISO-8859-1')
	accuracy=topic_compare(comp,10,400)
	# accuracy=topic_compare(comp,101,111,jump=2)
	print(accuracy)


		

