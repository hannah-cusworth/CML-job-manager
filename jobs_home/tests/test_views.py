from django.test import Client, TestCase, SimpleTestCase, TransactionTestCase
from jobs_home.views import *
from django.contrib.auth.models import User
from jobs_home.forms import *

# Templates
template_base = 'jobs_home/base.html'
template_pagination = 'jobs_home/pagination.html'
template_tables = 'jobs_home/tables.html'
template_client_card = 'jobs_home/client-card.html'
template_address_card = 'jobs_home/address-card.html'
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

dataset_size = 20

def create_object_set():
    address = Address(line_one="foo", city="bar", county="Derby", postcode="baz")
    person = Person(first="foo", last="bar", email="baz", number="123")
    address.save()
    person.save()
    address.client.add(person.pk)
    person.address.add(address.pk)
    job = Job(description="foo", client=person, job_address=address, billing_address=address)
    job.save()

class DetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(0 ,dataset_size):
            create_object_set()
        
        
       
    def test_data(self):
        self.assertEqual(Job.objects.all().count(), dataset_size)
        self.assertEqual(Address.objects.all().count(), dataset_size)
        self.assertEqual(Person.objects.all().count(), dataset_size)

class JobViewTest(DetailViewTest):
    def setUp(self):
        self.client = Client()
        self.job_id = Job.objects.first().pk
        self.job = Job.objects.get(pk=self.job_id)
        self.view = '/job/' + str(self.job_id)
        self.not_found = '/job/' + str(Job.objects.last().pk + 1)
        self.template = 'jobs_home/jobs.html'
        log_in(self.client)
        
    def test_jobview_get_status(self):
        response = self.client.get(self.view)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)
        self.assertTemplateUsed(response, template_detail)
        self.assertTemplateUsed(response, template_client_card)
        self.assertTemplateUsed(response, template_address_card)
    
    def test_jobview_404(self):
        response = self.client.get(self.not_found)
        self.assertEqual(response.status_code, 404)
        #nb assertRaiseError can't be used to test 404 error
    
    def test_jobview_get_context(self):
        response = self.client.get(self.view)
        self.assertEqual(response.context['job'], self.job)
        self.assertEqual(response.context['address'], Address.objects.get(pk=self.job.job_address_id))
        self.assertEqual(response.context['client'], Person.objects.get(pk=self.job.client_id))
    
    def test_jobview_post_status(self):
        response = self.client.post(self.view)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)
        self.assertTemplateUsed(response, template_detail)
        self.assertTemplateUsed(response, template_client_card)
        self.assertTemplateUsed(response, template_address_card)
    
    def test_jobview_post_edit(self):
        new_text = "edit"
        response = self.client.post(self.view, data={'description': new_text})
        self.job.refresh_from_db()          #NB you have to refresh, v imp
        self.assertEqual(self.job.description, new_text)
        
        

class ClientViewTest(DetailViewTest):
    def setUp(self):
        self.client = Client()
        self.client_id = Person.objects.first().pk
        self.person = Person.objects.get(pk=self.client_id)
        self.view = '/client/' + str(self.client_id)
        self.not_found = '/client/' + str(Person.objects.last().pk + 1)
        self.template = 'jobs_home/clients.html'
        log_in(self.client)
    
    def test_clientview_get_status(self):
        response = self.client.get(self.view)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)
        self.assertTemplateUsed(response, template_detail)
        self.assertTemplateUsed(response, template_client_card)

    def test_clientview_404(self):
        response = self.client.get(self.not_found)
        self.assertEqual(response.status_code, 404)
        
    def test_clientview_context(self):
        response = self.client.get(self.view)
        self.assertEqual(response.context['client'], self.person)
        self.assertQuerysetEqual(response.context['related'].order_by('id'), self.person.address.all().order_by('id'), transform= lambda x:x)
        self.assertQuerysetEqual(response.context['jobs'].order_by('id'), Job.objects.filter(client_id = self.person.pk).order_by('id'), transform= lambda x: x)

    def test_clientview_post_edit(self):
        new_text = "edit"
        response = self.client.post(self.view, data={'first': new_text})
        self.person.refresh_from_db()          
        self.assertEqual(self.person.first, new_text)

class AddressViewTest(DetailViewTest):
    def setUp(self):
        self.client = Client()
        self.address_id = Address.objects.first().pk
        self.address = Address.objects.get(pk=self.address_id)
        self.view = '/address/' + str(self.address_id)
        self.not_found = '/address/' + str(Address.objects.last().pk + 1)
        self.template = 'jobs_home/address.html'
        log_in(self.client)
    
    def test_addressview_get_status(self):
        response = self.client.get(self.view)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)
        self.assertTemplateUsed(response, template_detail)
        self.assertTemplateUsed(response, template_address_card)
    
    def test_addressview_404(self):
        response = self.client.get(self.not_found)
        self.assertEqual(response.status_code, 404)
    
    def test_addressview_context(self):
        response = self.client.get(self.view)
        self.assertEqual(response.context['address'], self.address)
        #by default transforms first item to a str using repr(). Overriden this with lambda so that it will literally compare the qs
        self.assertQuerysetEqual(response.context['related'], self.address.client.all().order_by('pk'), transform=lambda x: x)
        self.assertQuerysetEqual(response.context['jobs'].order_by('pk'), Job.objects.filter(job_address=self.address_id).order_by('pk'), transform=lambda x:x)
    
    def test_addressview_post_edit(self):
        new_text = "edit"
        response = self.client.post(self.view, data={'line_one': new_text})
        self.address.refresh_from_db()          #NB you have to refresh, v imp
        self.assertEqual(self.address.line_one, new_text)
    
           