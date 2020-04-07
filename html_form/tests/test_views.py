from django.test import SimpleTestCase, Client, TestCase
from html_form.views import *
from html_form.models import *

def check_context(func, response, *args):
    for arg in args:
        func.assertIn(arg, response)

def create_forms(job_postcode="SW1A 1AA", billing_postcode="SW1A 1AA", first="foo", description="foobar"):   
    return {'job-line_one':"foo",
    'job-line_two': "bar",
    'job-city': "foobar",
    'job-county': "Derby",
    'job-postcode':job_postcode,
    'billing-line_one':"foo",
    'billing-line_two':"bar",
    'billing-city': "foobar",
    'billing-county':"Derby",
    'billing-postcode': billing_postcode,
    'first':first,
    'last':"foo",
    'email':"a@a.com",
    'number':"0303 123 7300",
    'description':description,}  

def check_db_empty():
    if Person.objects.all() or Job.objects.all() or Address.objects.all():
        return False
    else:
        return True

'''def fetch_qs():
    return [client, addresses, job]'''

class FormViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.view = '/form/new/'
        self.form = 'html_form/form.html'
        self.success = 'html_form/success.html'

    def test_formview_get_status(self):
        response = self.client.get(self.view)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.form)
        check_context(self, response.context, 'jobaddress', 'billingaddress', 'client', 'job')

    def test_formview_post_status(self):
        response = self.client.post(self.view)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.form)
        check_context(self, response.context, 'jobaddress', 'billingaddress', 'client', 'job')

    def test_default_form_returns_success(self):
        data = create_forms()
        response = self.client.post(self.view, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.success)
        self.assertFalse(check_db_empty())

    def test_invalid_job_returns_form(self):
        data = create_forms(description="")
        response = self.client.post(self.view, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.form) 
    
    def test_invalid_job_db_empty(self):
        data = create_forms(description="")
        response = self.client.post(self.view, data=data)
        self.assertTrue(check_db_empty())      
    
    def test_invalid_jobaddress_returns_form(self):
        data = create_forms(job_postcode="foo")
        response = self.client.post(self.view, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.form)
    
    def test_invalid_jobaddress_db_empty(self):
        data = create_forms(job_postcode="foo")
        response = self.client.post(self.view, data=data)
        self.assertTrue(check_db_empty())    
    
    def test_invalid_client_returns_form(self):
        data = create_forms(first="123")
        response = self.client.post(self.view, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.form)
    
    def test_invalid_client_db_empty(self):
        data = create_forms(first="123")
        response = self.client.post(self.view, data=data)
        self.assertTrue(check_db_empty())
    
    def test_invalid_billing_returns_form(self):
        data = create_forms(billing_postcode="foo")
        response = self.client.post(self.view, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.form)
    
    def test_invalid_billing_db_empty(self):
        data = create_forms(billing_postcode="foo")
        response = self.client.post(self.view, data=data)
        self.assertTrue(check_db_empty())
    
    def test_valid_saves_correct_count_of_entries(self):
        data = create_forms()
        response = self.client.post(self.view, data=data)
        client = Person.objects.all()
        addresses = Address.objects.all()
        job = Job.objects.all()
        self.assertEqual(client.count(), 1)
        self.assertEqual(job.count(), 1)
        self.assertIn(addresses.count(), [1,2])

    '''def test_client_address_relationships(self):
        data = create_forms()
        response = self.client.post(self.view, data=data)
        client = Person.objects.all()
        addresses = Address.objects.all()
        for address in addresses:
            self.assertIn(client.pk, address.owner.all())
            self.assertIn(address.pk, client.address.all())'''
    

    
    


    

