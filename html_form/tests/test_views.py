from django.test import SimpleTestCase, Client, TestCase
from html_form.views import *

def check_context(func, response, *args):
    for arg in args:
        func.assertIn(arg, response)

class FormViewTest(SimpleTestCase):
    def test_formview_get(self):
        self.client = Client()
        response = self.client.get('/form/new/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'html_form/form.html')
        check_context(self, response.context, 'jobaddress', 'billingaddress', 'client', 'job')
    

class FormViewSavingTest(TestCase):
    #def submit_forms(self): 
    def test_test(self):
        self.client = Client()
        line_one="foo"
        line_two="bar"
        city="foobar"
        county="Derby"
        postcode="SW1A 1AA"
        
        first="foo"
        last="bar"
        email="a@a.com"
        number="0303 123 7300"
        description="foobar"
        response = self.client.post('/form/new', secure=False, follow=True, data={'first':first, 'last':last, 'number':number, 'email': email, 'description':description, 'job_line_one': line_one, 'job_line_two': line_two, 'job_city': city, 'job_county': county, 'job_postcode': postcode,'billing_line_one': line_one, 'billing_line_two': line_two, 'billing_city': city, 'billing_county': county, 'billing_postcode': postcode})
        
        
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'html_form/success.html')
    

