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
        jobaddressform = AddressForm()
        billingaddressform = AddressForm()
        clientform = ClientForm()
        jobform = JobForm()
        return render(request, self.template_name, {'billingaddress': billingaddressform, 'jobaddress': jobaddressform, 'client': clientform, 'job': jobform})
    
    def post(self, request):
        jobaddressform = AddressForm(request.POST)
        billingaddressform = AddressForm(request.POST)
        clientform = ClientForm(request.POST)
        jobform = JobForm(request.POST)
        
        if clientform.is_valid():
            new_client = clientform.save()
            if jobaddressform.is_valid():
                
                new_address_job = jobaddressform.save()
                new_address.client.add(new_client.id)
                new_client.address.add(new_address_job.id)
                if jobform.is_valid():
                    description = jobform.cleaned_data['description']
                    new_job = jobform.save(commit=False)
                    new_job.job_address = new_address_job.id
                    new_job.client_id = new_client.id
                #check whether billing address is empty 
                #if so, set the job billing address to the job address
                    if billingaddressform is None:
                        new_job.billing_address = new_address_job.id
                        new_job.save()
                        return render(request, "html_form/success.html")
                    elif billingaddressform.is_valid():
                
                        new_address_billing = billingaddressform.save()
                        new_address_billing.client.add(new_client.id)
                        new_client.address.add(new_address_billing.id)
                        new_job.billing_address = new_address_billing.id
                    
                        new_job.save()
                        return render(request, "html_form/success.html")
        
        return render(request, self.template_name, {'billingaddress': billingaddressform, 'jobaddress': jobaddressform, 'client': clientform, 'job': jobform})

        
        

        
       


        