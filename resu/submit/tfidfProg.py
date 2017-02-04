#!/usr/bin/env
print('Hello')
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.metrics.pairwise import cosine_similarity
from scipy import  sparse, io
import csv

filenames = ['jobListingOH.tsv','jobListingPA.tsv']
diceData = []
for filename in filenames:
  reader = csv.reader(open(filename, 'r'),delimiter = '\t')
 
  for row in reader:
    #print(row)
    diceData.append(row)
#print(d)
docIDCorpus = []
corpus = []
for post in diceData:
  #print(post)
  docIDCorpus.append('D' + post[4])
  corpus.append(post[5])
  docIDCorpus.append('C' + post[4])
  corpus.append(post[6])
#print(docIDCorpus)
#docIDCorpus.append('Hello')
vectorizer = TfidfVectorizer(min_df=1)
tfidf = vectorizer.fit_transform(corpus)
#print(tfidf)
csCoeff =cosine_similarity(tfidf) 
#print(csCoeff)
#tfidfFile = open('tfidf.mtx','wb+')
#tfidfFile.write(tfidf)
#print('Printing 1')
#io.mmwrite(tfidfFile,tfidf)
#csCoeffFile = open('cosineSimilarity.mtx','wb+')
#csCoeffFile.write(csCoeff)
#print('Printing2')
#io.mmwrite(csCoeffFile, csCoeff)
#ind0 = docIDCorpus.index('Hello')
#print(ind0)
ind1 = docIDCorpus.index('Chttp://www.dice.com/job/result/10105424/5902642-156?src=19')
ind2 =  docIDCorpus.index('Chttp://www.dice.com/job/result/10105424/5900266-600?src=19')
print(csCoeff[ind1,ind2])
print(corpus[ind1])
print('two')
print(corpus[ind2])
print('Done')

