from django.test import SimpleTestCase, Client, TestCase
from html_form.views import *
from html_form.models import *

def check_context(func, response, *args):
    for arg in args:
        func.assertIn(arg, response)

def create_forms(job_postcode="SW1A 1AA", billing_postcode="SW1A 1AA", first="foo", description="foobar", include_billing=True):   
    if include_billing:
        billing = "Derby"
    else:
        billing = ""
        billing_postcode = ""
        
    return {'job-line_one':"foo",
    'job-line_two': "bar",
    'job-city': "foobar",
    'job-county': "Derby",
    'job-postcode':job_postcode,
    'billing-line_one': billing,
    'billing-line_two': billing,
    'billing-city': billing,
    'billing-county': billing,
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



class FormViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.view = '/form/new/'
        self.form = 'html_form/form.html'
        self.success = 'html_form/success.html'
        self.person = Person.objects.all()
        self.addresses = Address.objects.all()
        self.job = Job.objects.all()
        

    def test_formview_get_status(self):
        response = self.client.get(self.view)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.form)
        check_context(self, response.context, 'jobaddress', 'billingaddress', 'client', 'job', 'billing_status')

    def test_formview_post_status(self):
        response = self.client.post(self.view)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.form)
        check_context(self, response.context, 'jobaddress', 'billingaddress', 'client', 'job', 'billing_status')

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
        self.assertEqual(self.person.count(), 1)
        self.assertEqual(self.job.count(), 1)
        self.assertIn(self.addresses.count(), [1,2])

    def test_valid_include_billing_addresses_types(self):
        data = create_forms()
        response = self.client.post(self.view, data=data)
        self.assertEqual(self.addresses.filter(address_type="JOB").count(), 1)
        self.assertEqual(self.addresses.filter(address_type="BILL").count(), 1)
    
    def test_valid_no_billing_addresses_types(self):
        data = create_forms(include_billing=False)
        response = self.client.post(self.view, data=data)
        self.assertEqual(self.addresses.count(), 1)
        self.assertEqual(self.addresses.filter(address_type="JOB").count(), 1)
        self.assertEqual(self.addresses.filter(address_type="BILL").count(), 0)

    def test_valid_client_address_relationships(self):
        data = create_forms()
        response = self.client.post(self.view, data=data)
       
        for address in self.addresses:
            self.assertIn(self.person.get(), address.client.all())
            self.assertIn(address, self.person.get().address.all())
    
    def test_valid_include_billing_job_relationships(self):
        data = create_forms()
        response = self.client.post(self.view, data=data)
        self.assertEqual(self.job.get().job_address, self.addresses.get(address_type="JOB"))
        self.assertEqual(self.job.get().billing_address, self.addresses.get(address_type="BILL"))

    def test_valid_no_billing_job_relationships(self):
        data = create_forms(include_billing=False)
        response = self.client.post(self.view, data=data)
        self.assertEqual(self.job.get().job_address, self.addresses.get())
        self.assertEqual(self.job.get().billing_address, self.addresses.get())

    


    

