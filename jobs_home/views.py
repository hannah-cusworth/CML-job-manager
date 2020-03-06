from django.shortcuts import render
from django.http import HttpResponse

def current(request):
    return render(request, "jobs_home/current.html")

def archive(request):
    return render(request, "jobs_home/archive.html")

def inbox(request):
    return render(request, "jobs_home/inbox.html")
