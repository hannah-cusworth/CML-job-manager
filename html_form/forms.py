from django import forms 
from html_form.models import Address, Client, Job
from crispy_forms.helper import FormHelper
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget
from crispy_forms.layout import Layout, Row, Column, Submit
from localflavor.gb.forms import GBCountySelect, GBPostcodeField


class AddressForm(forms.ModelForm):
    postcode = GBPostcodeField()
    class Meta:
        model = Address
        fields = ['line_one', 'line_two', 'city', 'county', 'postcode',]
        exclude = ['client']
        widgets = {
            'county': GBCountySelect()
        }
        labels = {
            'line_one': "Address 1",
            'line_two': "Address 2",
        }

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'line_one',
            'line_two',
            Row(
                Column('city', css_class='form-group col-md-6 mb-0'),
                Column('county', css_class='form-group col-md-4 mb-0'),
                Column('postcode', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            )
        )




class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = ['first', 'last', 'email', 'number']
        exclude = ['address']
        widgets = {
            'number': PhoneNumberInternationalFallbackWidget,
        }
        labels = {
            "first": "First Name",
            'last': "Last Name",
            "number": "Contact Number"
        }

    def __init__(self, *args, **kwargs) :
        super(ClientForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('first', css_class='form-group col-md-6 mb-0'),
                Column('last', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('email', css_class='form-group col-md-6 mb-0'),
                Column('number', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ) 
        )
       
class JobForm(forms.ModelForm):
   
    
    class Meta:
        model = Job
        fields = ['description']
        exclude = ['creation_date', 'status', 'address_id', 'client_id']
        widgets = {
            'description': forms.Textarea(attrs={'rows':4})
        }







