from django.test import Client, TestCase, SimpleTestCase
from jobs_home.views import *
from django.contrib.auth.models import User
from jobs_home.forms import *

# Templates
template_base = 'jobs_home/base.html'
template_pagination = 'jobs_home/pagination.html'
template_tables = 'jobs_home/tables.html'
template_client_card = 'jobs_home/client-card.html'
template_address_card = 'jobs_home/client-card.html'
template_detail = 'jobs_home/details.html'




class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.view = '/login'
        self.template = 'jobs_home/login.html'
        self.success = 'jobs_home/login.html'
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.success_data = {'username': 'john', 'password': 'johnpassword'}
        self.fail_data = {'username': "foo", "password": "bar"}

    def test_loginview_get_status(self):
        response = self.client.get(self.view)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)
        self.assertEqual(response.context["error"], "")
        self.assertIsInstance(response.context["form"], LoginForm)
        

    def test_loginview_post_status_success(self):
        response = self.client.post(self.view, data=self.success_data)
        self.assertRedirects(response, '/')
        
    def test_loginview_post_status_failure(self):
        response = self.client.post(self.view, data=self.fail_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)
        self.assertEqual(response.context["error"], "Login failed!")
        self.assertIsInstance(response.context["form"], LoginForm)

    def test_currentview_without_login(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/login?next=/')
    
    def test_inboxview_without_login(self):
        response = self.client.get('/inbox')
        self.assertRedirects(response, '/login?next=/inbox')
    
    def test_archiveview_without_login(self):
        response = self.client.get('/archive')
        self.assertRedirects(response, '/login?next=/archive')
    
    ##make sure to test detail views authentication######

def log_in(client): 
    user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    client.force_login(user)
def check_templates(self, response):
        self.assertTemplateUsed(response, self.template)
        self.assertTemplateUsed(response, template_base)
        self.assertTemplateUsed(response, template_pagination)
        self.assertTemplateUsed(response, template_tables)

class InboxViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.view = '/inbox'
        self.template = 'jobs_home/inbox.html'
        log_in(self.client)

    def test_inboxview_get_status(self):
        response = self.client.get(self.view)
        self.assertEqual(response.status_code, 200)
        check_templates(self, response)
    
    def test_inboxview_get_context(self):
        response = self.client.get(self.view)
        self.assertTrue(response.context["include_button"])


class CurrentViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.view = '/'
        self.template = 'jobs_home/current.html'
        log_in(self.client)

    def test_loginview_get_status(self):
        response = self.client.get(self.view)
        self.assertEqual(response.status_code, 200)
        check_templates(self, response)
    
    def test_currentview_get_context(self):
        response = self.client.get(self.view)
        self.assertTrue(response.context["include_button"])

class ArchiveViewTest():

    def setUp(self):
        self.client = Client()
        self.view = '/archive'
        self.template = 'jobs_home/archive.html'

    def test_loginview_get_status(self):
        response = self.client.get(self.view)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)

class DetailViewTest(TestCase):
    def setUpDatabase():
        address = Address(line_one="foo", city="bar", county="Derby", postcode="baz")
        person = Person(first="foo", last="bar", email="baz", number="123")
        address.save()
        person.save()
        job = Job(description="foo", client=client, job_address=address, billing_address=address)
        job.save()

class JobViewTest(DetailViewTest):
    def setUp(self):
        self.client = Client()
        self.view = '/job/' + Job.objects.get().pk
        self.tempate = 'jobs_home/jobs.html'
        log_in(self.client)
        
    def test_jobview_get_status(self):
        response = self.client.get(self.view)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)
        self.assertTemplateUsed(response, template_detail)
        self.assertTemplateUsed(response, template_client_card)
        self.assertTemplateUsed(response, template_address_card)

#class ClientViewTest():

#class AddressViewTest():
