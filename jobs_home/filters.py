import django_filters
from html_form.models import *
from django import forms 
from crispy_forms.layout import Layout, Row, Column, Submit
from crispy_forms.helper import FormHelper
from .forms import *






class ClientFilter(django_filters.FilterSet):

    class Meta:
        model = Client
        fields = ['first', 'last', 'email', 'number',]
   



class JobFilter(django_filters.FilterSet):
    class Meta:
        model = Job
        fields = ['description', 'creation_date',]

class AddressFilter(django_filters.FilterSet):
    class Meta:
        model = Address
        fields = ['line_one', 'city', 'county', 'postcode',]