from django.views.generic import TemplateView 
from django.shortcuts import render
from html_form.forms import AddressForm, ClientForm, JobForm 
   
class FormView(TemplateView):
    template_name = "html_form/form.html"
    
    def get(self, request):
        context = {
            "jobaddress": AddressForm(prefix='job'),
            "billingaddress": AddressForm(prefix="billing"),
            "client": ClientForm(),
            "job": JobForm(),
            "billing_status": "unbound",
        }
       
        return render(request, self.template_name, context)
    
    def post(self, request):
        jobaddressform = AddressForm(request.POST, prefix="job")
        billingaddressform_original = AddressForm(request.POST, prefix="billing")
        clientform = ClientForm(request.POST)
        jobform = JobForm(request.POST)

        #Establish whether billing address submitted.
        #If unused, set billingaddressform equal to jobaddressform to pass validation.
        if billingaddressform_original.empty():
            billingaddressform = jobaddressform
            billing_status = "unused"
        else:
            billingaddressform = billingaddressform_original
            billing_status = "used"

        #Validate forms 
        if clientform.is_valid() and jobform.is_valid() and jobaddressform.is_valid() and billingaddressform.is_valid():
            new_client = clientform.save(commit=False)
            new_job = jobform.save(commit=False)
            new_job_address = jobaddressform.save(commit=False)

            #If a billing address was submitted, save it as a separate entry in the database
            #Else, set it equal to the address object already saved
            if billing_status == "used":
                new_billing_address = billingaddressform.save(commit=False)
                new_billing_address.address_type = "BILL"
                new_billing_address.save()
                 
            else:
                new_billing_address = new_job_address
            
            #Create relationships between job, client and addresses
            
            #Add foreign keys (must be before saving)
            new_job.client = new_client
            new_job.billing_address = new_billing_address
            new_job.job_address = new_job_address
            #Save to db 
            new_client.save()
            new_job_address.save()
            new_job.save()
            #Add ManytoMany relationships (must be after saving)
            new_client.address.add(new_job_address.pk, new_billing_address.pk)
            new_job_address.client.add(new_client.pk)
            new_billing_address.client.add(new_client.pk)
            
            

            return render(request, "html_form/success.html")

        
        #If any of the forms fail validation, return bound forms.
        context = {
            'billingaddress': billingaddressform_original, 
            'jobaddress': jobaddressform, 
            'client': clientform, 
            'job': jobform, 
            'billing_status': billing_status
        }
        return render(request, self.template_name, context)

        
        
    
        
        

        
       


        