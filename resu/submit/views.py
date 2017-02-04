from django.shortcuts import render
from django.http import HttpResponse
from tfidfProg import applicant,company 
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

# Create your views here.

def index(request):
  if request.POST.get("req","") == "upload":
    resume = request.FILES['resume']
    github = request.POST['github']
    path = default_storage.save('tmp/'+resume.name, ContentFile(resume.read()))
    tmp_file = os.path.join(settings.MEDIA_ROOT, path)
    [company_matches, position_matches] = applicant(path,github)
    return render(
      request,
      'options.html',
      context={"company_matches":company_matches,"position_matches":position_matches}
    )
  if request.POST.get("req","") == "people":
    files = request.FILES['file']
    employees = company(files,culture,job)
    return render(
      request,
      'results.html',
      context={"matches": employees}
    )
  return render (
   request,
   'index.html',
   context={'subtitle':'Home'}
  )


