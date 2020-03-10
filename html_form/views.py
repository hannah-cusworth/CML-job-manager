from django.views.generic import TemplateView 
from django.shortcuts import render, redirect
from django.http import HttpResponse
from html_form.forms import AddressForm, ClientForm, JobForm
from datetime import datetime

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
            #maybe write a function here later
            first = clientform.cleaned_data['first']
            last = clientform.cleaned_data['last']
            email = clientform.cleaned_data['email']
            number = clientform.cleaned_data['number']
            new_client = clientform.save()
        if addressform.is_valid():
            line_one = addressform.cleaned_data['line_one']
            line_two = addressform.cleaned_data['line_two']
            city = addressform.cleaned_data['city']
            county = addressform.cleaned_data['county']
            postcode = addressform.cleaned_data['postcode']
            new_address = addressform.save()
            new_address.client.add(new_client.id)
            new_client.address.add(new_address.id)
            print("#############################################################################")
            print(new_address.id)

        if jobform.is_valid():
            description = jobform.cleaned_data['description']
            new_job = jobform.save(commit=False)
            address_id = new_address.id
            client_id = new_client.id
            status = 'Inbox'
            creation_date = datetime.now()
            new_job.save()




        return redirect('/')


        