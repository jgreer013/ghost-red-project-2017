#!/usr/bin/env

import json
import requests
import csv
from bs4 import BeautifulSoup
import re

def getJobListings(state):
  jobListing = csv.writer(open('jobListing' + state + '.tsv','wb+'),delimiter = '\t')
  pageCount = 1 
  r = requests.get('http://service.dice.com/api/rest/jobsearch/v1/simple.json?page=')
  finishListing = False;
  while (finishListing == False):
    print(pageCount)
    r = requests.get('http://service.dice.com/api/rest/jobsearch/v1/simple.json?state=' + state + '&page=' + str(pageCount))
    parsed_json = json.loads(r.text)
    
    for i in parsed_json['resultItemList']:
      #print(i)
      scrapDice = getJobDetails(i['detailUrl'].encode('utf-8'))
      jobListing.writerow([i['date'].encode('utf-8'),i['jobTitle'].encode('utf-8'),i['company'].encode('utf-8'),i['location'].encode('utf-8'),i['detailUrl'].encode('utf-8'),scrapDice[0],scrapDice[1],scrapDice[2]])
    if (parsed_json['count'] == parsed_json['lastDocument']):
      finishListing = True
    else:
      pageCount = pageCount +1

def getJobDetails(jobLink):
  reHref = re.compile('href=[\'"]?([^\'" >]+)')
  #print('Here')
  r = requests.get(jobLink)
  soup = BeautifulSoup(r.content,'lxml')
  #jobDetails = open('jobOrg.txt','wb+')
  #jobDetails.write(soup.prettify().encode('utf-8'))
  desc =  (soup.select("div#jobdescSec"))
  if (len(desc) != 0):
    desc = cleanhtml(str(desc[0]).decode('ascii','ignore'))
  else:
    desc=''
  compDes = soup.select("div.mTB20")
  if (len(compDes) != 0):
    compDes  = cleanhtml(str((compDes[0])).decode('ascii','ignore'))
  else:
    compDes = ''
  compLink = soup.select('a[href^="https://www.dice.com/company/"]')
  #print(compLink[0])
  if (len(compLink) != 0):
    compLink  = re.findall(reHref,str(compLink[0]))
    if (len(compLink) != 0):
      compLink  = compLink[0]
    else:
      compLink = ''
  else:
    compLink = ''
  #print(compLink)
  #desc = soup.find_all(['h1','h2'],attrs={'class':'jobdesc'})
  #print(desc)
  #print('COMPDESSSSSSSSSSSSSSSSS')
  #print(compDes)
  #nt('End')
  return [desc,compDes,compLink]
  #print(soup.findAll('h2',class_='jobdesc'))
  #jobDetails = open('job1.txt','wb+')
  #jobDetails.write(text.encode('utf-8')) 

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  cleantext = re.sub(r'\s\n\t\r','',cleantext)
  cleantext = cleantext.replace('&amp;','&')

  return cleantext

print('Hello')
getJobListings('PA')
print('Done')
