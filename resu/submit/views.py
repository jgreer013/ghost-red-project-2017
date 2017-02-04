from django.shortcuts import render
from django.http import HttpResponse
#from tfidfProg import applicant,company 

# Create your views here.

def index(request):
  if request.POST.get("req","") == "upload":
    resume = request.FILES['resume']
    github = request.POST['github']
    [company_matches, position_matches] = applicant(resume,github)
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


