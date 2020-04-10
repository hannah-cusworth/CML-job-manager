from django.test import TestCase
from html_form. models import Job, Address

class JobModelTest(TestCase):      

    def test_default_status(self):
        job = Job()
        
        self.assertEqual(job.status, "IN")


class AddressModelTest(TestCase):
    
    def test_default_address_type(self):
        address = Address()
        
        self.assertEqual(address.address_type, "JOB")

    
    
    