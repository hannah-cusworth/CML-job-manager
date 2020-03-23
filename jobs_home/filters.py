import django_filters
from html_form.models import *
from django import forms 
from crispy_forms.layout import Layout, Row, Column, Submit
from crispy_forms.helper import FormHelper
from .forms import *
from django.db.models import Q






class ClientFilter(django_filters.FilterSet):

    class Meta:
        model = Client
        fields = ['first', 'last', 'email', 'number',]
        



class JobFilter(django_filters.FilterSet):
    client_details = django_filters.CharFilter(method='client_name_search', label="Client Details")
    address_details = django_filters.CharFilter(method='address_search', label="Address Details")
    
    
    class Meta:
        model = Job
        fields = ['description', 'creation_date',]
        filter_overrides = {
        models.DateTimeField: {
            'filter_class': django_filters.DateFromToRangeFilter,
        }
    }
    
    def client_name_search(self, queryset, name, value):
        return queryset.filter(
            Q(client__first__icontains=value) | Q(client__last__icontains=value)
        )
    def address_search(self, queryset, name, value):
        return queryset.filter(
            Q(job_address__line_one__icontains=value) | Q(job_address__city__icontains=value) | Q(job_address__postcode__icontains=value)
        )

class AddressFilter(django_filters.FilterSet):
    class Meta:
        model = Address
        fields = ['line_one', 'city', 'county', 'postcode',]