from django.shortcuts import render
from django.http import HttpResponse
import jobs_home.models

def index(request):
    if request.method == "GET":
        return render(request, "html_form/index.html")
   
