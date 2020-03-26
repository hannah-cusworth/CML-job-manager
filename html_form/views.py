from django.views.generic import TemplateView 
from django.shortcuts import render, redirect
from django.http import HttpResponse
from html_form.forms import AddressForm, ClientForm, JobForm, BillingForm
from django.forms import ValidationError


def index(request):
        return render(request, "html_form/index.html")
   
class FormView(TemplateView):
    template_name = "html_form/form.html"
    
    def get(self, request):
        jobaddressform = AddressForm(prefix='job')
        billingaddressform = AddressForm( prefix="billing")
        clientform = ClientForm()
        jobform = JobForm()
        return render(request, self.template_name, {'billingaddress': billingaddressform, 'jobaddress': jobaddressform, 'client': clientform, 'job': jobform})
    
    def post(self, request):
        jobaddressform = AddressForm(request.POST, prefix="job")
        billingaddressform = AddressForm(request.POST, prefix="billing")
        clientform = ClientForm(request.POST)
        jobform = JobForm(request.POST)
        
        if clientform.is_valid():
            new_client = clientform.save(commit=False)
            if jobaddressform.is_valid():
                new_address_job = jobaddressform.save(commit=False)
                
                if jobform.is_valid():
                    new_job = jobform.save(commit=False)

                    if billingaddressform.is_valid():
                        new_address_job.save()
                        new_client.save()
                        new_address_billing = billingaddressform.save(commit=False)
                        
                        if new_address_billing.line_one == "":
                            new_job.billing_address = new_address_job
                        else:
                            new_address_billing.save()
                            new_job.billing_address = new_address_billing
                            new_address_billing.client.add(new_client.id)
                            new_client.address.add(new_address_billing.id)

                        new_job.job_address = new_address_job
                        new_job.client_id = new_client.id
                        
                        new_job.save()  
                        
                        new_address_job.client.add(new_client.id)
                        new_client.address.add(new_address_job.id)

                        return render(request, "html_form/success.html")
        
        return render(request, self.template_name, {'billingaddress': billingaddressform, 'jobaddress': jobaddressform, 'client': clientform, 'job': jobform})

        
        

        
       


        