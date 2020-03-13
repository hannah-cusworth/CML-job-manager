from django.views.generic import TemplateView 
from django.shortcuts import render, redirect
from django.http import HttpResponse
from html_form.forms import AddressForm, ClientForm, JobForm
from django.forms import ValidationError


def index(request):
        return render(request, "html_form/index.html")
   
class FormView(TemplateView):
    template_name = "html_form/form.html"
    
    def get(self, request):
        addressform = AddressForm()
        clientform = ClientForm()
        jobform = JobForm()
        return render(request, self.template_name, {'address': addressform, 'client': clientform, 'job': jobform})
    
    def post(self, request):
        addressform = AddressForm(request.POST)
        clientform = ClientForm(request.POST)
        jobform = JobForm(request.POST)
        
        if clientform.is_valid():
            new_client = clientform.save()
            if addressform.is_valid():
                
                new_address = addressform.save()
                new_address.client.add(new_client.id)
                new_client.address.add(new_address.id)
                if jobform.is_valid():
                    description = jobform.cleaned_data['description']
                    new_job = jobform.save(commit=False)
                    new_job.address_id = new_address.id
                    new_job.client_id = new_client.id
                
                    new_job.save()
                    
                    return render(request, "html_form/success.html")
        
        return render(request, self.template_name, {'address': addressform, 'client': clientform, 'job': jobform})

        
        

        
       


        