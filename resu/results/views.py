from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
  return render(
    request,
    'results.html',
    context={"matches":request.POST.get("matches")}
  )

def matchInfo(request):
  return render(
    request,
    'matchinfo.html',
    context={"culture":request.GET.get("culture")*100,
      "position": request.GET.get("position")*100})
