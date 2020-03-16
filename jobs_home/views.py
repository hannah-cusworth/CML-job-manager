from django.shortcuts import render
from django.http import HttpResponse, Http404
from html_form.models import Job

def current(request):
    context = {
        "current_jobs": [job for job in Job.objects.all() if job.status == "CU"]
    }
    return render(request, "jobs_home/current.html", context)

def archive(request):
    return render(request, "jobs_home/archive.html")

def inbox(request):
    context = {
        "current_jobs": [job for job in Job.objects.all() if job.status == "IN"]
    }
    return render(request, "jobs_home/inbox.html", context)

def jobs(request, job_id):
    try:
        job = Job.objects.get(pk=job_id)
    except Job.DoesNotExist:
        raise Http404("Job does not exist")
    context = {
        "job": job,
    }
    return render(request, "jobs_home/jobs.html", context)
