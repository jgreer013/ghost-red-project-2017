#!/usr/bin/env python
import textract
import re

def extractResumeText(filename):
  # extracts resume data from documents of many formats (docx, pdf, odf, etc.)
  text = textract.process(filename)
  email = re.search(r"([A-Za-z0-9_\-+]+@[A-Za-z0-9_\-+.]+\.[A-Za-z]+)+", text)
  nonemail = re.sub(r"([A-Za-z0-9_\-+]+@[A-Za-z0-9_\-+.]+\.[A-Za-z]+)+", "", text)
  urls  = re.search(r"([A-Za-z0-9\-.]+\.[A-Za-z]+)+", nonemail)
  retdict = {"email":None,"urls":None}
  retdict["text"]=re.sub(r"[^A-Za-z0-9\s\-]","",text).split()
  if email is not None:
    retdict["email"]=email.groups()
  if urls is not None:
    retdict["urls"]=urls.groups()
  return retdict

# Test on sample resume:
# print extractResumeText("./resume.pdf")
