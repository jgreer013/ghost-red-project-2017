import re
import urllib
from bs4 import BeautifulSoup
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
import tldextract
 
def getWebpageText(url):
    tld = tldextract.extract(url).registered_domain
    try:
        html = urllib.urlopen(url)
    except:
        return []
    soup = BeautifulSoup(html, 'lxml')
    #data = soup.findAll(text=True)

    links = soup.findAll('a')
    first_order = []
    for link in links:
        k = link.get('href')
        if tldextract.extract(str(k)).registered_domain == tld and k not in first_order:
            first_order.append(k)
     
    def visible(element):
        if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
            return False
        elif re.match('<!--.*-->', str(element.encode('utf-8'))):
            return False
        return True
    data = soup.findAll(text=True)

    result = filter(visible, data)
    
    
    for link in first_order:
        k = urllib.urlopen(str(link))
        soup = BeautifulSoup(k, 'lxml')
        data2 = soup.findAll(text=True)
        data.extend(data2)

    rez = []
    for each in result:
      all_split = each.encode("utf8").split(" ")
      for word in all_split:
        if (word.isalnum()):
          rez.append(word)
    return rez


def word_feats(words):
    return dict([(word, False) for word in words])

def getSentiment(list_of_words):
 
    negids = movie_reviews.fileids('neg')
    posids = movie_reviews.fileids('pos')
     
    negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
    posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]
     
    negcutoff = len(negfeats)*3/4
    poscutoff = len(posfeats)*3/4
     
    trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
    #testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]
    print 'train on %d instances' % (len(trainfeats))
     
    classifier = NaiveBayesClassifier.train(trainfeats)

    testfeats = [(word_feats(list_of_words), '')]
    results = classifier.classify_many([fs for (fs, l) in testfeats])
    return results[0]





