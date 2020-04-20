from django.test import Client, TestCase, SimpleTestCase, TransactionTestCase
from jobs_home.filters import * 
from .test_views import CreateData, no_transform

class FiltersTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        CreateData.create_object_set()
        CreateData.create_object_set_multiple_clients()
        CreateData.create_object_set_multiple_jobs()
        CreateData.create_object_set_with_billing()
        CreateData.create_object_set_jobfilter_addressdetails()
        CreateData.create_object_set_jobfilter_clientname()

class ClientFilterTest(FiltersTest):
    def setUp(self):
        self.qs = Person.objects.all()
    
    def test_clientfilter_first(self):
        filtered = ClientFilter({"first": "2"}, queryset=self.qs)
        self.assertQuerysetEqual(filtered.qs.order_by('pk'), Person.objects.filter(first__icontains="2").order_by('pk'), transform=no_transform)
    
    def test_clientfilter_last(self):
        filtered = ClientFilter({"last": "2"}, queryset=self.qs)
        self.assertQuerysetEqual(filtered.qs.order_by('pk'), Person.objects.filter(last__icontains="2").order_by('pk'), transform=no_transform)
   
    def test_clientfilter_number(self):
        filtered = ClientFilter({"number": "2"}, queryset=self.qs)
        self.assertQuerysetEqual(filtered.qs.order_by('pk'), Person.objects.filter(number__icontains="2").order_by('pk'), transform=no_transform)

    def test_clientfilter_email(self):
        filtered = ClientFilter({"email": "2"}, queryset=self.qs)
        self.assertQuerysetEqual(filtered.qs.order_by('pk'), Person.objects.filter(email__icontains="2").order_by('pk'), transform=no_transform)

class AddressFilterTest(FiltersTest):
    def setUp(self):
        self.qs = Address.objects.all()
    
    def test_addressfilter_lineone(self):
        filtered = AddressFilter({"line_one": "bill"}, queryset=self.qs)
        self.assertQuerysetEqual(filtered.qs.order_by('pk'), Address.objects.filter(line_one__icontains="bill").order_by('pk'), transform=no_transform)
    
    def test_addressfilter_city(self):
        filtered = AddressFilter({"city": "bill"}, queryset=self.qs)
        self.assertQuerysetEqual(filtered.qs.order_by('pk'), Address.objects.filter(city__icontains="bill").order_by('pk'), transform=no_transform)
    
    def test_addressfilter_county(self):
        filtered = AddressFilter({"county": "bill"}, queryset=self.qs)
        self.assertQuerysetEqual(filtered.qs.order_by('pk'), Address.objects.filter(county__icontains="bill").order_by('pk'), transform=no_transform)
    
    def test_addressfilter_postcode(self):
        filtered = AddressFilter({"postcode": "bill"}, queryset=self.qs)
        self.assertQuerysetEqual(filtered.qs.order_by('pk'), Address.objects.filter(postcode__icontains="bill").order_by('pk'), transform=no_transform)

class JobFilterTest(FiltersTest):
    def setUp(self):
        self.qs = Job.objects.all()
        
    
    def test_jobfilter_description(self):
        filtered = JobFilter({"description": "2"}, queryset=self.qs)
        self.assertQuerysetEqual(filtered.qs.order_by('pk'), Job.objects.filter(description__icontains="2").order_by('pk'), transform=no_transform)

    def test_jobfilter_clientdetails(self):
        filtered = JobFilter({"client_details": "qw"}, queryset=self.qs)
        self.assertEqual(filtered.qs.count(), 2)

    def test_jobfilter_addressdetails(self):
        filtered = JobFilter({"address_details": "qw"}, queryset=self.qs)
        self.assertEqual(filtered.qs.count(), 4)

        

