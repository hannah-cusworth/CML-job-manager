from django.test import SimpleTestCase, Client
from html_form.views import *

class FormViewTest(SimpleTestCase):
    def test_get(self):
        self.client = Client()
        self.client.last="bob"
        #response = self.client.get('/form/new/')
        #self.assertEqual(response.status_code, 200)
        #elf.assertEqual(response.templates, 'html_form/new.html')
