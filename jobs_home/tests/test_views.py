from django.test import Client, TestCase, SimpleTestCase
from jobs_home.views import *
from django.contrib.auth.models import User

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

    def test_loginview_post_status_success(self):
        response = self.client.post(self.view, data=self.success_data)
        self.assertRedirects(response, '/')
        
    def test_loginview_post_status_failure(self):
        response = self.client.post(self.view, data=self.fail_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)

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


class InboxViewTest():
    def setUp(self):
        self.client = Client()
        self.view = '/inbox'
        self.template = 'jobs_home/inbox.html'

    def test_loginview_get_status(self):
        response = self.client.get(self.view)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)

class CurrentViewTest():
    def setUp(self):
        self.client = Client()
        self.view = '/'
        self.template = 'jobs_home/current.html'

    def test_loginview_get_status(self):
        response = self.client.get(self.view)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)

class ArchiveViewTest():
    def setUp(self):
        self.client = Client()
        self.view = '/archive'
        self.template = 'jobs_home/archive.html'

    def test_loginview_get_status(self):
        response = self.client.get(self.view)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)

#class JobViewTest():

#class ClientViewTest():

#class AddressViewTest():
