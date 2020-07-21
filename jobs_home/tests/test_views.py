from django.test import Client, TestCase, SimpleTestCase, TransactionTestCase
from jobs_home.views import *
from django.contrib.auth.models import User
from jobs_home.forms import *
from jobs_home.filters import *
from django.db.models import Q

# Templates
template_base = 'jobs_home/base.html'
template_pagination = 'jobs_home/pagination.html'
template_tables = 'jobs_home/tables.html'
template_client_card = 'jobs_home/client-card.html'
template_address_card = 'jobs_home/address-card.html'
template_detail = 'jobs_home/details.html'

#by default transforms first item to a str using repr(). Overriden this with lambda so that it will literally compare the qs
no_transform = lambda x:x
dataset_size = 20

def log_in(client): 
    user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    client.force_login(user)

class CreateData():

    def create_object_set():
        address = Address(line_one="foo", city="bar", county="Derby", postcode="baz")
        person = Person(first="foo", last="bar", email="baz", number="123")
        address.save()
        person.save()
        address.client.add(person.pk)
        person.address.add(address.pk)
        job = Job(description="foo", client=person, job_address=address, billing_address=address)
        job.save()
        return {"person": person, "job": job, "address": address}

    def create_object_set_with_billing():
        object_set = CreateData.create_object_set()
        address_2 = Address(line_one="billing", city="billing", county="billing", postcode="billing", address_type="BILL")
        address_2.save()
        object_set["person"].address.add(address_2.pk)
        address_2.client.add(object_set["person"].pk)
        object_set["job"].billing_address = address_2
        object_set["address_2"] = address_2 
        return object_set

    def create_object_set_multiple_clients():
        object_set = CreateData.create_object_set()
        person_2 = Person(first="person_2", last="person_2", email="person_2", number="person_2")
        person_2.save()
        person_2.address.add(object_set["address"].pk)
        object_set["address"].client.add(person_2.pk)
        object_set["person_2"] = person_2
        return object_set

    def create_object_set_multiple_jobs():
        object_set = CreateData.create_object_set()
        object_set["job_2"]  = Job(description="job_2", client=object_set["person"], job_address=object_set["address"], billing_address=object_set["address"])
        object_set["job_2"].save()
        return object_set
    
    def create_object_set_jobfilter_clientname():
        attributes = ["first", "last"]
        for attribute in attributes:
            object_set = CreateData.create_object_set()
            setattr(object_set["person"], attribute, "qwerty")
            object_set["person"].save()
    
    def create_object_set_jobfilter_addressdetails():
        attributes = ["line_one", "city", "county", "postcode"]
        for attribute in attributes:
            object_set = CreateData.create_object_set()
            setattr(object_set["address"], attribute, "qwerty")
            object_set["address"].save()
        


class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.view = '/login'
        self.template = 'jobs_home/login.html'
        self.success = 'jobs_home/login.html'
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.success_data = {'username': 'john', 'password': 'johnpassword'}
        self.fail_data = {'username': "foo", "password": "bar"}
        self.data_with_space = {'username': ' john ', 'password': 'johnpassword'}

    def test_loginview_get_status(self):
        response = self.client.get(self.view)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)
        self.assertEqual(response.context["error"], "")
        self.assertIsInstance(response.context["form"], LoginForm) 

    def test_loginview_post_status_success(self):
        response = self.client.post(self.view, data=self.success_data)
        self.assertRedirects(response, '/')
    
    def test_loginview_username_strips_spaces(self):
        response = self.client.post(self.view, data=self.data_with_space)
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
    
    # Tests for detail views without logins with their 
    # respective test classes as they require db setup

class ListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
            CreateData.create_object_set()
    
    def check_templates(self, response):
        self.assertTemplateUsed(response, self.template)
        self.assertTemplateUsed(response, template_base)
        self.assertTemplateUsed(response, template_pagination)
        self.assertTemplateUsed(response, template_tables)

class InboxViewTest(ListViewTest):
    def setUp(self):
        self.client = Client()
        self.view = '/inbox'
        self.post_view = '/'
        self.template = 'jobs_home/inbox.html'
        self.job = Job.objects.get()
        self.job_id = self.job.pk
        log_in(self.client)

    def test_inboxview_get_status(self):
        response = self.client.get(self.view)
        self.assertEqual(response.status_code, 200)
        self.check_templates(response)
    
    def test_inboxview_get_context(self):
        response = self.client.get(self.view)
        self.assertTrue(response.context["button_label_one"])
        self.assertTrue(response.context["button_label_two"])     

    def test_inboxview_post_changejobstatus(self):
        response = self.client.post(self.post_view, data={"id": self.job_id, "status": 2})
        self.job.refresh_from_db()
        self.assertEqual(self.job.status, "CU")

class CurrentViewTest(ListViewTest):
    def setUp(self):
        self.client = Client()
        self.view = '/'
        self.job = Job.objects.get()
        self.job_id = self.job.pk
        self.template = 'jobs_home/current.html'
        log_in(self.client)

    def test_loginview_get_status(self):
        response = self.client.get(self.view)
        self.assertEqual(response.status_code, 200)
        self.check_templates(response)
    
    def test_currentview_get_context(self):
        response = self.client.get(self.view)
        self.assertTrue(response.context["button_label_one"])
        self.assertTrue(response.context["button_label_two"]) 
    
    def test_currentview_post_status(self):
        response = self.client.post(self.view, data={"status": 1})
        self.assertEqual(response.status_code, 200)
        self.check_templates(response)

    def test_currentview_post_changejobstatus_to_archive(self):
        response = self.client.post(self.view, data={"id": self.job_id, "status": 3})
        self.job.refresh_from_db()
        self.assertEqual(self.job.status, "AR")

class ArchiveViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.view = '/archive'
        self.template = 'jobs_home/archive.html'
        log_in(self.client)

    def test_archiveview_get_status(self):
        response = self.client.get(self.view)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)
    
    '''def test_archiveview_get_context(self):
        context = ArchiveView.get_context(self)
        self.assertIsInstance(context["job_search"], JobFilter)
        self.assertEqual(context["address_search"], AddressFilter)
        self.assertEqual(context["client_search"], ClientFilter)'''
    


class DetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(0 ,dataset_size):
            CreateData.create_object_set()
       
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
    
    def check_templates(self, response):
        self.assertTemplateUsed(response, self.template)
        self.assertTemplateUsed(response, template_detail)
        self.assertTemplateUsed(response, template_client_card)
        self.assertTemplateUsed(response, template_address_card)

    def test_jobview_get_status(self):
        response = self.client.get(self.view)
        self.assertEqual(response.status_code, 200)
        self.check_templates(response)

    def test_addressview_without_login(self):
        logout(self.client)
        response = self.client.get(self.view)
        self.assertRedirects(response, '/login?next='+self.view)
    
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
    
    def test_jobview_post_status(self):
        response = self.client.post(self.view)
        self.assertEqual(response.status_code, 200)
        self.check_templates(response)
    
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
    
    def check_templates(self, response):
        self.assertTemplateUsed(response, self.template)
        self.assertTemplateUsed(response, template_detail)
        self.assertTemplateUsed(response, template_client_card)
    
    def test_clientview_get_status(self):
        response = self.client.get(self.view)
        self.assertEqual(response.status_code, 200)
        self.check_templates(response)
    
    def test_clientview_without_login(self):
        logout(self.client)
        response = self.client.get(self.view)
        self.assertRedirects(response, '/login?next='+self.view)
        
    def test_clientview_404(self):
        response = self.client.get(self.not_found)
        self.assertEqual(response.status_code, 404)
        
    def test_clientview_context(self):
        response = self.client.get(self.view)
        self.assertEqual(response.context['client'], self.person)
        self.assertQuerysetEqual(response.context['related'].order_by('id'), self.person.address.all().order_by('id'), transform=no_transform)
        self.assertQuerysetEqual(response.context['jobs'].order_by('id'), Job.objects.filter(client_id = self.person.pk).order_by('id'), transform=no_transform)

    def test_clientview_context_2_jobs(self):
        object_set = CreateData.create_object_set_multiple_jobs()
        client_id = object_set["person"].pk
        response = self.client.get("/client/" + str(client_id))
        self.assertQuerysetEqual(response.context['jobs'].order_by('pk'), Job.objects.filter(client_id=client_id).order_by('pk'), transform=no_transform)
    
    def test_clientview_context_with_billing(self):
        object_set = CreateData.create_object_set_with_billing()
        client_id = object_set["person"].pk
        response = self.client.get("/client/" + str(client_id))
        self.assertQuerysetEqual(response.context['related'].order_by('pk'), Address.objects.filter(client=client_id).order_by('pk'), transform=no_transform)

    def test_clientview_post_status(self):
        response = self.client.post(self.view)
        self.assertEqual(response.status_code, 200)
        self.check_templates(response)

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
    
    def check_templates(self, response):
        self.assertTemplateUsed(response, self.template)
        self.assertTemplateUsed(response, template_detail)
        self.assertTemplateUsed(response, template_address_card)
    
    def test_addressview_get_status(self):
        response = self.client.get(self.view)
        self.assertEqual(response.status_code, 200)
        self.check_templates(response)
    
    def test_addressview_without_login(self):
        logout(self.client)
        response = self.client.get(self.view)
        self.assertRedirects(response, '/login?next='+self.view)
    
    def test_addressview_404(self):
        response = self.client.get(self.not_found)
        self.assertEqual(response.status_code, 404)
    
    def test_addressview_context(self):
        response = self.client.get(self.view)
        self.assertEqual(response.context['address'], self.address)
        self.assertQuerysetEqual(response.context['related'], self.address.client.all().order_by('pk'), transform=no_transform)
        self.assertQuerysetEqual(response.context['jobs'].order_by('pk'), Job.objects.filter(Q(job_address_id=self.address_id)|Q(billing_address_id=self.address_id)).order_by('pk'), transform=no_transform)
    
    def test_addressview_context_2_jobs(self):
        object_set = CreateData.create_object_set_multiple_jobs()
        address_id = object_set["address"].pk
        response = self.client.get("/address/" + str(address_id))
        self.assertQuerysetEqual(response.context['jobs'].order_by('pk'), Job.objects.filter(Q(job_address_id=address_id)|Q(billing_address_id=address_id)).order_by('pk'), transform=no_transform)

    def test_addressview_context_2_clients(self):
        object_set = CreateData.create_object_set_multiple_clients()
        address = object_set["address"]
        response = self.client.get("/address/" + str(address.pk))
        self.assertQuerysetEqual(response.context['related'].order_by('pk'), address.client.all().order_by('pk'), transform=no_transform )
    
    def test_addressview_post_status(self):
        response = self.client.post(self.view)
        self.assertEqual(response.status_code, 200)
        self.check_templates(response)

    def test_addressview_post_edit(self):
        new_text = "edit"
        response = self.client.post(self.view, data={'line_one': new_text})
        self.address.refresh_from_db()          #NB you have to refresh, v imp
        self.assertEqual(self.address.line_one, new_text)
    
'''class PaginationTest(TestCase):
    @classmethod
    def setUpTestData(cls):'''
        