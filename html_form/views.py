from django.views.generic import TemplateView 
from django.shortcuts import render, redirect
from django.http import HttpResponse
from html_form.forms import AddressForm, ClientForm, JobForm

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
            first = form.cleaned_data['first']
            last = form.cleaned_data['last']
            email = form.cleaned_data['email']
            number = form.cleaned_data['number']
            clientform.save()
        if addressform.is_valid():
            line_one = form.cleaned_data['line_one']
            line_two = form.cleaned_data['line_two']
            city = form.cleaned_data['city']
            county = form.cleaned_data['county']
            postcode = form.cleaned_data['postcode']
            addressform.save()
        if jobform.is_valid():
            description = form.cleaned_data['description']

        
        
        return redirect('jobs_home/')


        