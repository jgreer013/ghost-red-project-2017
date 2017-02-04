#!/usr/bin/env
print('Hello')
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.metrics.pairwise import cosine_similarity
from scipy import  sparse, io
import csv
from resume.py import extractResumeText(filename)
from GitHubDataTest.py import githubMessages(argv)
from webNltk.py import getWebpageText(url)


def applicant(resumeFileName,githubUserName):
  diceFileNames = ['jobListingOH.tsv','jobListingPA.tsv']
  diceData = []
  for filename in diceFileNames:
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

  resumeDict = extractResumeText(resumeFileName)
  if (resumeDict["url"] != None):
    webPageText = getWebpageText(resumeDict["url"])
    corpus.append(' '.join(webPageText))
    docIDCorpus.append('W'+resumeFileName)
  readGitOutFile = False
  if (githubUserName != None):
    githubMessages([githubUserName,'GitHubFetch.txt'])
    readGitOutFile = True
  else if (resumeDict['email'] != None):
    githubMessages([resumeDict['email'],'GitHubFetch.txt'])
    readGitOutFile = True
  else:
    readGitOutFile = False
  if (readGitOutFile == True):
    gitOutput = ''
    with open('GitHubFetch.txt') as f:
      for line in f.readlines():
        gitOutput = ' '.join(line.split())
  else:
    gitOutput = ''

  corpus.append(resumeDict["text"] + gitOutput)
  docIDCorpus.append('R'+resumeFileName)
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
  #print(csCoeff[ind1,ind2])
  #print(corpus[ind1])
  #print('two')
  #print(corpus[ind2])
  #print('Done')

