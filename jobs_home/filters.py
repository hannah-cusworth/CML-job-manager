import django_filters
from html_form.models import *
from django import forms 
from crispy_forms.layout import Layout, Row, Column, Submit
from crispy_forms.helper import FormHelper
from .forms import *
from django.db.models import Q
#from tempus_dominus.widgets import DatePicker

class ClientFilter(django_filters.FilterSet):
    first = django_filters.CharFilter(lookup_expr="icontains", label="First name")
    last = django_filters.CharFilter(lookup_expr="icontains", label="Last name")
    email = django_filters.CharFilter(lookup_expr="icontains", label="Email")
    number = django_filters.CharFilter(lookup_expr="icontains", label="Contact number")
    class Meta:
        model = Person
        fields = ['first', 'last', 'email', 'number',]
    
       
        
class AddressFilter(django_filters.FilterSet):
    line_one = django_filters.CharFilter(lookup_expr="icontains", label="Address 1")
    city = django_filters.CharFilter(lookup_expr="icontains", label="City")
    county = django_filters.CharFilter(lookup_expr="icontains", label="County")
    postcode = django_filters.CharFilter(lookup_expr="icontains", label="Postcode")
    class Meta:
        model = Address
        fields = ['line_one', 'city', 'county', 'postcode',]
        

class JobFilter(django_filters.FilterSet):
    client_details = django_filters.CharFilter(method='client_name_search', label="Client Name")
    address_details = django_filters.CharFilter(method='address_search', label="Address Details")
    description = django_filters.CharFilter(lookup_expr="icontains", label="Description")
    #widget not displaying correctly
    #creation_date = django_filters.DateFilter(field_name='creation_date', label="Date Created", widget=DatePicker)
    
    class Meta:
        model = Job
        fields = ['description',]
    
    def client_name_search(self, queryset, name, value):
        return queryset.filter(
            Q(client__first__icontains=value) | Q(client__last__icontains=value)
        )
    def address_search(self, queryset, name, value):
        return queryset.filter(
            Q(job_address__line_one__icontains=value) | Q(job_address__line_two__icontains=value) | Q(job_address__city__icontains=value) | Q(job_address__county__icontains=value) | Q(job_address__postcode__icontains=value)
        )


        