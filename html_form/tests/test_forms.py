from django.test import TestCase

class TestFormValidation(TestCase):
    def jobform_test():
        job = {"description": }
    
    def clientform_test():
        client = {"first": }

    def test_charfields(self):
        self.assertFieldOutput(CharField, {"1111111111111111111111111111111111111111111111111111111111111111": "1111111111111111111111111111111111111111111111111111111111111111"}, {"11111111111111111111111111111111111111111111111111111111111111111": "Invalid"})
