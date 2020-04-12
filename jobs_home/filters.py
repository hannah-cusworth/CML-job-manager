import django_filters
from html_form.models import *
from django import forms 
from crispy_forms.layout import Layout, Row, Column, Submit
from crispy_forms.helper import FormHelper
from .forms import *
from django.db.models import Q
#from tempus_dominus.widgets import DatePicker







class ClientFilter(django_filters.FilterSet):

    class Meta:
        model = Person
        fields = ['first', 'last', 'email', 'number',]
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            }
        }
        



class JobFilter(django_filters.FilterSet):
    client_details = django_filters.CharFilter(method='client_name_search', label="Client Details")
    address_details = django_filters.CharFilter(method='address_search', label="Address Details")
    #widget not displaying correctly
    #creation_date = django_filters.DateFilter(field_name='creation_date', label="Date Created", widget=DatePicker)
    
    
    class Meta:
        model = Job
        fields = ['description',]
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
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
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            }
        }