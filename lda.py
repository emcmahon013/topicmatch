import csv
import gensim
import logging, bz2
import nltk
from collections import defaultdict
import json

#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def recursive_node_to_dict(node):
    result = {
        'name': node.name,
    }
    children = [recursive_node_to_dict(c) for c in node.get_children()]
    if children:
        result['children'] = children
    return result



word_freq = {}
wordlist = []
tweets = []
with open('twits.csv', 'rb') as csvfile:
    twitsreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in twitsreader:
        stoplist = set('for a of the and to in is rt t.co / \\'.split())
        row = [word for word in str(row).lower().split() if word not in stoplist]
        for n in ('\'','rt','"','[',']','@','!', 'http',':','#','/','t.co',',','&',';',',','\\',')','(','.','?', '-'	): #remove meaningless characters
            row = str(row).replace(n,'')
        row=row.lower()
        tokenize = nltk.word_tokenize(row)
        tweets.append(tokenize)
        words = row.split()
        for word in words: #create wordlist for id2word dictionary mapping
			word = word.strip()
			word = unicode(word, "utf-8")
			word = nltk.word_tokenize(word)
			wordlist.append(word)
'''
for word in wordlist:
	word_freq = {i:words.count(i) for i in set(words)}
print word_freq				
'''
		
id2word = gensim.corpora.Dictionary(wordlist)
corpus = [id2word.doc2bow(tweet) for tweet in tweets]
#print id2word
lda = gensim.models.LdaModel(corpus, num_topics = 10,id2word=id2word)

topics= lda.show_topics(-1)
lda.save('lda.csv')
#print topics

clean_topics = []
probs = []
vals = []
json = '{ "name": "parent", "children": [ '
topicDict = defaultdict(list)
topicDict['names'].append('parent')
counter = 0
for topic in topics:
	counter = counter +1
	tempTopic = []
	tempProbs = []
	topic = topic.split(' + ')
	json = json + '{"name" : "topic' + str(counter) + '", "children": [ ' 
	topicDict['children'].append('topic' + str(counter))
	for word in topic:
		val = word.split('*')
		tempProbs.append(val[0])
		tempTopic.append(val[1])
		json = json + '{"name" : "' + val[1] + '", "size": ' + val[0] + '}, '
		topicDict['topic' + str(counter)].append((val[1],val[0]))
	json = json[:len(json)-2] + ']},'
	probs.append(tempProbs)
	clean_topics.append(tempTopic)

json = json[:len(json)-1] + ']}'
print json

json_string = json.dumps(topicDict)
f = open('topics.json', 'w')
print >> f,json_string
f.close()

with open('topics.csv', 'wb') as acsv:
    w = csv.writer(acsv)
    #w.writerow(('Tweet'))
    for topic in clean_topics:
        w.writerow(topic)


with open('probs.csv', 'wb') as acsv:
    w = csv.writer(acsv)
    #w.writerow(('Tweet'))
    for row in probs:
        w.writerow(row)