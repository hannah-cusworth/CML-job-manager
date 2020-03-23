from crispy_forms.layout import Layout, Row, Column, Submit
from crispy_forms.helper import FormHelper

class ClientFilterFormHelper(FormHelper):
    form_method="GET"
    form_id="client_form"
   

    layout = Layout(
        Row(
            Column('first', css_class="form-group col-md-5 mb-0"),
            Column('last', css_class="form-group col-md-5 mb-0"),
        ),
            
        Row(
            Column('number', css_class="form-group col-md-5 mb-0"),
            Column('email', css_class="form-group col-md-5 mb-0"),  
        ),
        Submit('submit', 'Submit', css_class='button')
    )

class JobFilterFormHelper(FormHelper):
    form_method="GET"
    form_id="job_form"
    
    layout = Layout(
        Row(
            Column('description', css_class="form-group col-md-5 mb-0"),
            Column('creation_date', css_class="form-group col-md-5 mb-0"),    
        ),
        Row(
            Column('client_details', css_class="form-group col-md-5 mb-0"),
            Column('address_details', css_class="form-group col-md-5 mb-0"), 
        ),
        Submit('submit', 'Submit', css_class='button'),
       
    )

class AddressFilterFormHelper(FormHelper):
    form_method="GET"
    form_id="address_form"
    labels={
        "line_one": "Address 1",
    }
    layout = Layout(
        Row(
            Column('line_one', css_class="form-group col-md-5 mb-0"),
            Column('city', css_class="form-group col-md-5 mb-0"),
        ),
            
        Row(
            Column('county', css_class="form-group col-md-5 mb-0"),
            Column('postcode', css_class="form-group col-md-5 mb-0"),
            
        ),
        Submit('submit', 'Submit', css_class='button'),
       
    )
