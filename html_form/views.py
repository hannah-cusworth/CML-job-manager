from django.views.generic import TemplateView 
from django.shortcuts import render, redirect
from django.http import HttpResponse
from html_form.forms import AddressForm, ClientForm, JobForm 
from django.forms import ValidationError

#what does this do?
def index(request):
        return render(request, "html_form/index.html")
   
class FormView(TemplateView):
    template_name = "html_form/form.html"
    
    def get(self, request):
        context = {
            "jobaddress": AddressForm(prefix='job'),
            "billingaddress": AddressForm(prefix="billing"),
            "client": ClientForm(),
            "job": JobForm(),
            "checkbox": "unbound",
        }
       
        return render(request, self.template_name, context)
    
    def post(self, request):
        jobaddressform = AddressForm(request.POST, prefix="job")
        billingaddressform_original = AddressForm(request.POST, prefix="billing")
        clientform = ClientForm(request.POST)
        jobform = JobForm(request.POST)

        if billingaddressform_original.empty:
            billingaddressform = jobaddressform
            checkbox = "checked"
        else:
            billingaddressform = billingaddressform_original
            checkbox = "foo"

       
        '''if clientform.is_valid() and jobform.is_valid() and jobaddressform.is_valid() and billingaddressform.is_valid():
            new_client = clientform.save(commit=False)
            new_job = jobform.save(commit=False)
            new_address_job = jobaddressform.save(commit=False)
            new_address_billing = billingaddressform.save(commit=False)'''
            

        
        
        
        
        
        
        
        
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
                            new_address_billing.address_type = "BILL"
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
        
        return render(request, self.template_name, {'billingaddress': billingaddressform_original, 'jobaddress': jobaddressform, 'client': clientform, 'job': jobform, "checkbox": checkbox})

        
        

        
       


        