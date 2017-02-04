#!/usr/bin/env
#print('Hello')
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.metrics.pairwise import cosine_similarity
from scipy import  sparse, io
import csv
from resume import extractResumeText
from GitHubDataTest import githubMessages
from webNltk import getWebpageText


def applicant(resumeFileName,githubUserName):
  diceFileNames = ['jobListingOH.tsv']#,'jobListingPA.tsv']
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
  foundWebsite = False
  resumeDict = extractResumeText(resumeFileName)
  #print(resumeDict["urls"])
  #print(resumeDict["email"])
  if (not (resumeDict["urls"] is None) and resumeDict["urls"] != '' ):
    webPageText = getWebpageText(resumeDict["urls"][0])
    corpus.append(' '.join(webPageText))
    docIDCorpus.append('W'+resumeFileName)
    foundWebsite = True
  else:
    corpus.append('')
    docIDCorpus.append('W'+resumeFileName)
  #print(corpus[len(corpus)-1])
  readGitOutFile = False
  if (not (githubUserName is  None)):
    githubMessages(githubUserName, 'GitHubFetch')
    readGitOutFile = True
  elif (not (resumeDict['email'] is None)):
    githubMessages(resumeDict['email'], 'GitHubFetch')
    readGitOutFile = True
  else:
    readGitOutFile = False
  if (readGitOutFile == True):
    gitOutput = ''
    with open('GitHubFetch.tsv') as f:
      for line in f.readlines():
        gitOutput = ' '.join(line.split())
  else:
    gitOutput = ''
  #print('gitOut' + gitOutput)
  corpus.append(resumeDict["text"] + gitOutput)
  docIDCorpus.append('R'+resumeFileName)
  vectorizer = TfidfVectorizer(min_df=1)
  tfidf = vectorizer.fit_transform(corpus)
  returnResultSet1 = []
  returnResultSet2 = []
  csCoeff =cosine_similarity(tfidf) 
  #print(csCoeff)
  print(len(diceData))
  print(len(diceData[0]))
  if (foundWebsite == True):
    resultSet1 = getSortedMax((csCoeff[len(csCoeff)-1][0:len(csCoeff[0])-1]).tolist(),docIDCorpus[0:len(docIDCorpus)-1])
    resultSet2 = getSortedMax((csCoeff[len(csCoeff)-2][0:len(csCoeff[0])-2]).tolist(),docIDCorpus[0:len(docIDCorpus)-2])
    
    for key in resultSet1[0]:
      for x in range(0,len(diceData)):
        if (diceData[x][4] == key[1:]):
          tempInd=x
          returnResultSet1.append([diceData[tempInd][1],diceData[tempInd][4],diceData[tempInd][3]])
          break
    for key in resultSet2[0]:
      for x in range(0,len(diceData)):
        if (diceData[x][4] == key[1:]):
          tempInd=x
          returnResultSet2.append([diceData[tempInd][2],diceData[tempInd][7]])
          break
  else:
    resultSet = getSortedMax((csCoeff[len(csCoeff)-1][0:len(csCoeff[0])-1]).tolist(),docIDCorpus[0:len(docIDCorpus)-1])
    for key in resultSet1[0]:
      for x in range(0,len(diceData)):
        if (diceData[x][4] == key[1:]):
          tempInd=x
          returnResultSet1.append([diceData[tempInd][1],diceData[tempInd][4],diceData[tempInd][3]])
          breaks
  print(returnResultSet1)
  print(returnResultSet2)
  return [returnResultSet1,returnResultSet2]
def company(resumeFileNames, CompanyDesc, JobDesc):
  print('Hi')

def getSortedMax(csScoreRow,keys):
  x1 = 0
  mydict = {}
  #print(len(keys))
  #print(len(csScoreRow))
  for key in keys:
  	mydict[key] = csScoreRow[x1]
	x1 += 1
  x=0
  #print(mydict)
  #return "hi"
  returnDict = [[],[]]
  for key2,csScoreRow2 in sorted(mydict.iteritems(),key=lambda(k,v):(v,k),reverse = True):
    if ( x< 10):
      returnDict[0].append(key2)
      returnDict[1].append(csScoreRow2)
      x = x + 1
    else:
      return returnDict
"""
def mergeSort(ls,keys):
    if len(ls) <= 1:
        return ls
    else:
        mid = len(ls)/2
        left = mergeSort(ls[:mid])
        right = mergeSort(ls[mid:])
        left_pt = 0
        right_pt = 0
        length = len(left)+len(right)
        ret = [0]*length
        retKeys = [0]*length
        for x in xrange(len(left)+len(right)):
            if left_pt == len(left):
                ret[x] = right[right_pt]
                retKeys[x] = keys[right_pt]
                right_pt += 1
            elif right_pt == len(right):
                ret[x] = left[left_pt]
                retKeys[x] = keys[left_pt]
                left_pt += 1
            else:
                l = left[left_pt]
                keyl = key[left_pt]
                r = right[right_pt]
                keyr = key[right_pt]
                if l <= r:
                    ret[x] = l
                    retKeys[x] = keyl
                    left_pt += 1
                elif r < l:
                    ret[x] = r
                    retKeys[x] = keyr
                    right_pt += 1
return [ret,retKeys]
"""

#applicant('BakerFN_Resume.pdf','frazierbaker')
