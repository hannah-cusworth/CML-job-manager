from django.shortcuts import render, redirect 
from django.http import HttpResponse, Http404, HttpRequest
from html_form.models import Job, Address, Person
from django.views.generic import TemplateView, ListView 
from django.template import RequestContext
from jobs_home.filters import *
from jobs_home.forms import *
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q


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
          
class InboxView(LoginRequiredMixin, TemplateView):
    template_name = "jobs_home/inbox.html"

    def get(self, request):
        current_jobs = Job.objects.filter(status="IN").order_by('id')
        page_obj = paginate(current_jobs, request)

        context = {
            "job_results": page_obj,
            "page_obj": page_obj, 
            "include_button": True,                 ###???
            "button_label": "Move to Current"       ### move this      
        }

        return render(request, self.template_name, context)

    def post(self, request):
        id_num = request.POST.get("id")
        try:
            job = Job.objects.get(pk=id_num)
            job.status="CU"
            job.save()
        except:
            pass
        
        return render(request, self.template_name)

class CurrentView(LoginRequiredMixin, ListView):
    template_name = "jobs_home/current.html"
    def get(self, request):
         
        current_jobs = Job.objects.filter(status="CU").order_by('id')
        page_obj = paginate(current_jobs, request)

        context = {
            "job_results": page_obj,
            "current_jobs": page_obj,
            "include_button": True,                     ###!!
            "button_label": "Move to Archive",             ##!!
        }

        return render(request, self.template_name, context)   
    
    def post(self, request):
        id_num = request.POST.get("id")
        try:
            job = Job.objects.get(pk=id_num)
            job.status="AR"
            job.save()
        except:
            pass
        
        return render(request, self.template_name)

class ArchiveView(LoginRequiredMixin, ListView):
    template_name = "jobs_home/archive.html"
   
    def get(self, request):
        context = self.get_context()

        if 'client_btn' in request.GET:
            page_obj = self.filter_client(request)
            context["client_results"] = page_obj

        if 'address_btn' in request.GET:
            page_obj = self.filter_address(request)
            context["address_results"] = page_obj

        if 'job_btn' in request.GET:
            page_obj = self.filter_job(request)
            context["job_results"] = page_obj
        
        try:
            context["page_obj"] = page_obj
        except:
            pass
        
        context["query"] = self.get_query(request)

        return render(request, self.template_name, context)
           
    
    def filter_client(self, request):
        filtered = ClientFilter(request.GET, queryset=Person.objects.all().order_by('id'))
        return paginate(filtered.qs,request)


    def filter_address(self, request):
        filtered = AddressFilter(request.GET, queryset=Address.objects.all().order_by('id'))
        return paginate(filtered.qs,request)
        

    def filter_job(self, request):
        filtered = JobFilter(request.GET, queryset=Job.objects.all().order_by('id'))
        return paginate(filtered.qs,request)
        
    def get_context(self):
        client_search = ClientFilter()
        client_search.form.helper = ClientFilterFormHelper()
        job_search = JobFilter()
        job_search.form.helper = JobFilterFormHelper()
        address_search = AddressFilter()
        address_search.form.helper = AddressFilterFormHelper()

        context = {
            "job_search": job_search,
            "client_search": client_search,
            "address_search": address_search,
        }

        return context

    def get_query(self, request):
        try:
            query = request.META["QUERY_STRING"]
            if "page=" in query:
                i = query.find("page=")
                i -= 1
                query = query[:i]
            return query
        except:
            return None
        

    
class JobView(LoginRequiredMixin, TemplateView):
    template_name = "jobs_home/jobs.html"
    
    def get(self, request, job_id):
        try:
            job = Job.objects.get(pk=job_id)
        except Job.DoesNotExist:
            raise Http404("Job does not exist")

        context = {
            "job": job,                                                 #!!!
            "address": Address.objects.get(pk=job.job_address_id),
            "client": Person.objects.get(pk=job.client_id),
            "background": "background-color: #79a6d2",                  #!!!
            "click": True,
        }
   
        return render(request, self.template_name, context)
  
   
    def post(self, request, job_id):
        job = Job.objects.get(pk=job_id)
        post = request.POST 
        keys = post.keys()    
        
        for column in keys:
            setattr(job, column, post[column])
            job.save()
        
        return render(request, self.template_name)

class AddressView(LoginRequiredMixin, TemplateView):
    template_name = "jobs_home/address.html"

    def get(self, request, address_id):
        try:
            address = Address.objects.get(pk=address_id)

        except Address.DoesNotExist:
            raise Http404("Address does not exist")
        
        try:
            jobs = Job.objects.filter(Q(job_address_id=address_id)|Q(billing_address_id=address_id))
        except:
            jobs = []

        context = {
            "background": "background-color: #ffcc99",      #!!!
            "address": address,
            "related": address.client.all(),
            "jobs": jobs,
            "click": None,                                  #!!!
        }

        return render(request, self.template_name, context)
    
    def post(self,request, address_id):
        
        address = Address.objects.get(pk=address_id)
        post = request.POST 
        keys = post.keys()    
        
        for column in keys:
                setattr(address, column, post[column])
                address.save()
        
        return render(request, self.template_name,)

class ClientView(LoginRequiredMixin, TemplateView):
    template_name = "jobs_home/clients.html"

    def get(self, request, client_id):
        try:
            client = Person.objects.get(pk=client_id)
        except Person.DoesNotExist:
            raise Http404("Client does not exist")
        
        try:
            jobs = Job.objects.filter(client_id=client_id)
        except:
            jobs = []

        context = {
            "background": "background-color: #ff8080",                  #!!!
            "client": client,
            "related": client.address.all(),
            "jobs": jobs,
            "click": None,                                              #!!!
        }
            
        return render(request, self.template_name, context)
        
    
    def post(self,request, client_id,):
        client = Person.objects.get(pk=client_id)
        post = request.POST 
        keys = post.keys()    
        
        for column in keys:
                post[column].strip("&nbsp;") #contenteditable spaces are different
                setattr(client, column, post[column])
                client.save()

        return render(request, self.template_name)

def paginate(item, request):
    paginator = Paginator(item, 10) 
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
