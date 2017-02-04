from django.shortcuts import render
from django.http import HttpResponse
from uuid import uuid
import os



# Create your views here.

def index(request):
  UUID = str(uuid4())
  if request.POST.get("req","") == "upload":
    resume = request.FILES['resume']

  if request.POST.get("req","") == "people":
    files = request.FILES['file']
  return render(
    request,
    'submit/index.html',
    context={}
  )

