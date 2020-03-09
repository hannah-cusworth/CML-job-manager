from django import forms 
from html_form.models import Address, Client, Job


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['line_one', 'line_two', 'city', 'county', 'postcode']

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first', 'last', 'email', 'number']

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['description']
        exclude = ['creation_date', 'status', 'address', 'client']
