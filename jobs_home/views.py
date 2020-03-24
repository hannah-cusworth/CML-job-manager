from django.shortcuts import render
from django.http import HttpResponse, Http404
from html_form.models import Job, Address, Client
from django.views.generic import TemplateView, ListView 
from django.template import RequestContext
from jobs_home.filters import *
from .forms import *




def current(request):
    context = {
        "current_jobs": [job for job in Job.objects.all() if job.status == "CU"]
    }
    return render(request, "jobs_home/current.html", context)

class ArchiveView(ListView):
    template_name = "jobs_home/archive.html"

    def get(self, request):
        
        
        clients = ClientFilter()
        clients.form.helper = ClientFilterFormHelper()
        jobs = JobFilter()
        jobs.form.helper = JobFilterFormHelper()
        addresses = AddressFilter()
        addresses.form.helper = AddressFilterFormHelper()
     
        context = {
            "jobs": jobs,
            "clients": clients,
            "addresses": addresses,
            "current_clients": None,
            "current_jobs": None,
            "current_addresses": None,
            "display_job": "display:none",
            "display_client": "display:none",
            "display_address": "display:none",
        }

#rm first if
        if 'client_btn' in request.GET:
            context["current_clients"] = ClientFilter(request.GET, queryset=Client.objects.all())
            context["display_client"] = "display:block"
        elif 'job_btn' in request.GET:
            context["current_jobs"] = JobFilter(request.GET, queryset=Job.objects.all())
            context["display_job"] = "display:block"
        elif 'address_btn' in request.GET:
            context["current_addresses"] = AddressFilter(request.GET, queryset=Address.objects.all())
            context["display_address"] = "display:block"
        else:
            context["display_job"] = "display:block"

        return render(request, self.template_name, context)
    
    
        
        
    
   



        

class InboxView(TemplateView):
    template_name = "jobs_home/inbox.html"

    def get(self, request):
        context = {
            "current_jobs": [job for job in Job.objects.all() if job.status == "IN"]
        }
        return render(request, self.template_name, context)

    def post(self, request):
        idnum = request.POST.get("idnum")
        job = Job.objects.get(pk=idnum)
        job.status="CU"
        job.save()
        
        return render(request, self.template_name)

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
        print(request.POST)
        category = request.POST["card"]
        job = Job.objects.get(pk=job_id)
        if category == "client_info":
            category = Client.objects.get(pk=job.client_id)
        if category == "address_info":
            category = Address.objects.get(pk=job.job_address_id)
        if category == "job_info":
            category = Job.objects.get(pk=job_id)

        post = request.POST 
        keys = post.keys()    
        
        for column in keys:
    
            if column != "card":
                setattr(category, column, post[column])
                category.save()
        
        return render(request, self.template_name)

