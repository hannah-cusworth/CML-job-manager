from django.shortcuts import render
from django.http import HttpResponse, Http404
from html_form.models import Job, Address, Client
from django.views.generic import TemplateView 
from django.template import RequestContext


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

class JobView(TemplateView):
    template_name = "jobs_home/jobs.html"
   
    def get(self, request, job_id):
        try:
            job = Job.objects.get(pk=job_id)
        except Job.DoesNotExist:
            raise Http404("Job does not exist")
        context = {
            "job": job,
            "address": Address.objects.get(pk=job.job_address_id),
            "client": Client.objects.get(pk=job.client_id)
        }
        return render(request, self.template_name, context)
  
   
    def post(self, request, job_id):
        post = request.POST
        keys = post.keys()
        job = Job.objects.get(pk=job_id)
        print(job.description)
        
        for column in keys:
            setattr(job, column, post[column])
            job.save()
        print(job.description)
        
        
        return render(request, self.template_name)
