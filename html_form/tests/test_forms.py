from django.test import SimpleTestCase
from html_form.forms import *

class AddressFormTest(SimpleTestCase):
    def create_address_form(self,line_one="foo", line_two="bar", city="foobar", county="Derby", postcode="SW1A 1AA"):
        return AddressForm(data={'line_one': line_one, 'line_two': line_two, 'city': city, 'county': county, 'postcode': postcode})
        
    def test_default_is_valid(self):
        form = self.create_address_form()
        self.assertTrue(form.is_valid())
    
    def test_line_one_required(self):
        form = self.create_address_form(line_one="")
        self.assertFalse(form.is_valid())
    
    def test_line_two_not_required(self):
        form = self.create_address_form(line_two="")
        self.assertTrue(form.is_valid())

    def test_city_required(self):
        form = self.create_address_form(city="")
        self.assertFalse(form.is_valid())

    def test_county_required(self):
        form = self.create_address_form(county="")
        self.assertFalse(form.is_valid())

    def test_postcode_required(self):
        form = self.create_address_form(postcode="")
        self.assertFalse(form.is_valid())
    
    def test_county_options(self):
        form = self.create_address_form(county="foo")
        self.assertFalse(form.is_valid())
    
    def test_postcode_validator(self):
        form = self.create_address_form(postcode="foo")
        self.assertFalse(form.is_valid())
    
class JobFormTest(SimpleTestCase):
    def create_job_form(self, description="foobar"):
        return JobForm(data={'description': description,})
    
    def test_default_is_valid(self):
        form = self.create_job_form()
        self.assertTrue(form.is_valid())
    
    def test_description_required(self):
        form = self.create_job_form(description="")
        self.assertFalse(form.is_valid())
  

class ClientFormTest(SimpleTestCase):
    def create_client_form(self, first="foo", last="bar", email="a@a.com", number="0303 123 7300"):
        return ClientForm(data={'first': first, 'last': last, 'email': email, 'number': number})

    def test_default_is_valid(self):
        form = self.create_client_form()
        self.assertTrue(form.is_valid())
    
    def test_first_required(self):
        form = self.create_client_form(first="")
        self.assertFalse(form.is_valid())
    
    def test_last_required(self):
        form = self.create_client_form(last="")
        self.assertFalse(form.is_valid())

    def test_email_required(self):
        form = self.create_client_form(email="")
        self.assertFalse(form.is_valid())

    def test_number_required(self):
        form = self.create_client_form(number="")
        self.assertFalse(form.is_valid())

    def test_email_validator(self):
        form = self.create_client_form(email="foobar")
        self.assertFalse(form.is_valid())

    def test_number_validator(self):
        form = self.create_client_form(number="123")
        self.assertFalse(form.is_valid())

    def test_first_alpha(self):
        form = self.create_client_form(first="123")
        self.assertFalse(form.is_valid())

    def test_last_alpha(self):
        form = self.create_client_form(last="123")
        self.assertFalse(form.is_valid())

