import pandas as pd

def clean_topics(topics,csv=False):
	if csv==True:
		topics.rename(columns={'Unnamed: 0':'Symbol'}, inplace=True)
	else:
		topics['Symbol']=topics.index
	try:
		del topics['text']
	except:
		pass
	return topics


def aggregate(topics,comp,csv=False,std=True):
	topics=clean_topics(topics,csv)
	topics=pd.merge(topics,comp,on='Symbol')
	by_industry=topics.groupby('Industry')
	ind_med=by_industry.mean()
	ind_std=by_industry.std()
	if std==True:
		return ind_med,ind_std
	else:
		return ind_med


if __name__ == "__main__":
	file='/Users/erinmcmahon/mygit/topicmatch/COMP.csv'
	comp=pd.read_csv(file,encoding='ISO-8859-1')
	file='/Users/erinmcmahon/mygit/topicmatch/topic_list.csv'
	topics=pd.read_csv(file,encoding='ISO-8859-1')
	ind_med,ind_std=aggregate(topics,comp,csv=True)
	ind_med.to_csv('/Users/erinmcmahon/mygit/topicmatch/industry_topics.csv',sep=',')
	# file='/Users/erinmcmahon/mygit/topicmatch/topic_list2.csv'
	# topics=pd.read_csv(file,encoding='ISO-8859-1')
	# ind_topics2=aggregate(topics,comp)
	# ind_topics2.to_csv('/Users/erinmcmahon/mygit/topicmatch/industry_topics2.csv',sep=',')



