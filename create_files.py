import pandas as pd
import numpy as np
import os

def filewrite(path,text):
	f=open(path,'w')
	f.write(desc)
	f.close()
	return f

file='COMP.csv'
company=pd.read_csv(file,encoding='ISO-8859-1')
path='/Users/erinmcmahon/mygit/topicmatch/'

n=len(company)
for i in range(n):
	symbol=company['Symbol'][i]
	desc=company['Description'][i]
	if not os.path.exists('Symbol'):
		os.makedirs(symbol)
		directory=os.path.join(path,symbol)
		abstract=os.path.join(directory,'abstract.txt')
		paper=os.path.join(directory,'paper.txt')
		abstractfile=filewrite(abstract,desc)
		paperfile=filewrite(paper,desc)
	else:
		print("ERROR")



