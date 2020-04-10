from django.shortcuts import render, redirect 
from django.http import HttpResponse, Http404, HttpRequest
from html_form.models import Job, Address, Person
from django.views.generic import TemplateView, ListView 
from django.template import RequestContext
from jobs_home.filters import *
from .forms import *
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.mixins import LoginRequiredMixin


def logout_view(request):
    logout(request)
    return redirect("/login")


class LoginView(TemplateView):
    template_name = "jobs_home/login.html"

    def get(self, request):
        context = {
            "error": "",
            "form": LoginForm(),
        }
        
        return render(request, self.template_name, context)

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            context = {
            "error": "Login failed!",
            "form": LoginForm(request.POST),
            }
            return render(request, self.template_name, context)

class ArchiveView(LoginRequiredMixin, ListView):
    template_name = "jobs_home/archive.html"

    def get(self, request):
        try:
            query = request.META["QUERY_STRING"]
            if "page=" in query:
                i = query.find("page=")
                i -= 1
                query = query[:i]
        except:
            query = None
        
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
            "button": False,
            "query": query,
        }

#rm first if
        if 'client_btn' in request.GET:
            filtered = ClientFilter(request.GET, queryset=Person.objects.all().order_by('id'))
            page_obj = paginate(filtered.qs,request)
            context["current_clients"] = page_obj
            context["display_client"] = "display:block"

  
        elif 'job_btn' in request.GET:
            filtered = JobFilter(request.GET, queryset=Job.objects.all().order_by('id'))
            page_obj = paginate(filtered.qs,request)
            context["current_jobs"] = page_obj
            context["display_job"] = "display:block"
           
        elif 'address_btn' in request.GET:
            filtered = AddressFilter(request.GET, queryset=Address.objects.all().order_by('id'))
            page_obj = paginate(filtered.qs,request)
            context["current_addresses"] = page_obj
            context["display_address"] = "display:block"
        else: 
            context["display_job"] = "display:block"
            page_obj = None
        
        context["page_obj"] = page_obj

        return render(request, self.template_name, context)
    
    
        
class CurrentView(LoginRequiredMixin, ListView):
    template_name = "jobs_home/current.html"
    def get(self, request):
        
        current_jobs = Job.objects.filter(status="CU").order_by('id')
        page_obj = paginate(current_jobs, request)

        context = {
            "page_obj": page_obj,
            "current_jobs": page_obj,
            "button": True,
        }

        return render (request, self.template_name, context)      
          

class InboxView(LoginRequiredMixin, TemplateView):
    template_name = "jobs_home/inbox.html"

    def get(self, request):
        current_jobs = Job.objects.filter(status="IN").order_by('id')
        page_obj = paginate(current_jobs, request)

        context = {
            "current_jobs": page_obj,
            "button": True,
            "page_obj": page_obj
            
        }
        return render(request, self.template_name, context)

    def post(self, request):
        idnum = request.POST.get("idnum")
        job = Job.objects.get(pk=idnum)
        job.status="CU"
        job.save()
        
        return render(request, self.template_name)

class JobView(LoginRequiredMixin, TemplateView):
    template_name = "jobs_home/jobs.html"
    
    def get(self, request, job_id):
        try:
            job = Job.objects.get(pk=job_id)
        except Job.DoesNotExist:
            raise Http404("Job does not exist")
        context = {
            "job": job,
            "address": Address.objects.get(pk=job.job_address_id),
            "client": Person.objects.get(pk=job.client_id),
            "background": "background-color: #79a6d2",
            "click": True,
        }
   
        return render(request, self.template_name, context)
  
   
    def post(self, request, job_id):
        job = Job.objects.get(pk=job_id)
        post = request.POST 
        keys = post.keys()    
        
        for column in keys:
    
            if column != "card":
                setattr(job, column, post[column])
                job.save()
               
        
        return render(request, self.template_name)

class AddressView(LoginRequiredMixin, TemplateView):
    template_name = "jobs_home/address.html"

    def get(self, request, address_id):
        try:
            address = Address.objects.get(pk=address_id)
        except Job.DoesNotExist:
            raise Http404("Address does not exist")
        
        try:
            jobs_billing = Job.objects.filter(billing_address = address_id)
        except:
            jobs_billing = []
        
        try:
            jobs_work = Job.objects.filter(job_address = address_id)
        except:
            jobs_work = []


        context = {
            "background": "background-color: #ffcc99",
            "address": address,
            "related": address.client.all(),
            "jobs_billing": jobs_billing,
            "jobs_work": jobs_work,
            "click": None,
        }

        return render(request, self.template_name, context)
    
    def post(self,request, address_id):
        
        address = Address.objects.get(pk=address_id)
        post = request.POST 
        keys = post.keys()    
        
        for column in keys:
    
            if column != "card":
                setattr(address, column, post[column])
                address.save()
        
        return render(request, self.template_name, context)

class ClientView(LoginRequiredMixin, TemplateView):
    template_name = "jobs_home/clients.html"

    def get(self, request, client_id):
        try:
            client = Person.objects.get(pk=client_id)
        except Job.DoesNotExist:
            raise Http404("Client does not exist")
        
        try:
            jobs = Job.objects.filter(client_id=client_id)
        except:
            jobs = []
        


        context = {
            "background": "background-color: #ff8080",
            "client": client,
            "related": client.address.all(),
            "jobs": jobs,
            "click": None,
        }
            
        return render(request, self.template_name, context)
        
    
    def post(self,request, client_id,):
        client = Person.objects.get(pk=client_id)
        post = request.POST 
        keys = post.keys()    
        
        for column in keys:
    
            if column != "card":
                setattr(client, column, post[column])
                client.save()

        return render(request, self.template_name)

def paginate(item, request):
    paginator = Paginator(item, 10) 
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
