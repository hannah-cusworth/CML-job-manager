from django import forms 
from crispy_forms.layout import Layout, Row, Column, Submit
from crispy_forms.helper import FormHelper


class SearchForm(forms.Form):
    options = [
        ("first", "First name"),
        ("last", "Last name"),
        ('description', "Description"),
        ('line_one', "Address"),
        ("postcode", "Postcode"),
        ("email", "Email"),
        ("number", "Number"),
    ]
    category = forms.ChoiceField(choices=options)
    search_term = forms.CharField(max_length=64)

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = True
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Row(
                Column('category', css_class="form-group col-md-3 mb-0"),
                Column('search_term', css_class="form-group col-md-6 mb-0"),
                Submit('search', 'SEARCH', css_class="btn btn-primary col-md-1 mb-0")
            )
        )