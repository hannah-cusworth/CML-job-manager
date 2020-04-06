from django.test import TestCase
from django.utils import timezone
'''
class TestJobModel(TestCase):
    def create_job(
        self, 
        description="foo bar", 
        status="CU", 
        job_address=1, 
        billing_address=1, 
        client=1,):
        return Job.objects.create(creation_date=timezone.now(), description=description, status=status, job_address=job_address, billing_address=billing_address, client=client)
    
    def test_status(self):
        job = self.create_job
        '''