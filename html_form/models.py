from django.db import models
from datetime import datetime
from django.core.validators import validate_email
from phonenumber_field.modelfields import PhoneNumberField
from localflavor.gb.forms import GBCountySelect, GBPostcodeField
from .validators import validate_alpha



class Address(models.Model):
    client = models.ManyToManyField('Client', related_name="owner")
    line_one = models.CharField(max_length=64, )
    line_two = models.CharField(max_length=64, blank=True)
    city = models.CharField(max_length=64)
    county = models.CharField(max_length=64)
    postcode = models.CharField(max_length=64)
    creation_date = models.DateTimeField(
        auto_now_add=True
        )

   # def __str__(self):
        #return f"{self.line_one}, {self.line_two}, {self.city}, {self.county} {self.postcode}"



class Client(models.Model):
    first = models.CharField(
        max_length=64,
        validators=[validate_alpha],
        )
    last = models.CharField(
        max_length=64,
        validators=[validate_alpha],
        )
    email = models.EmailField(
        max_length=64, 
        validators=[validate_email]
        )
    number = PhoneNumberField()
    creation_date = models.DateTimeField(
        auto_now_add=True
        )
    address = models.ManyToManyField(Address, related_name="address")

    def __str__(self):
        return f"{self.first.capitalize} {self.last.capitalize}"


class Job(models.Model):
    INBOX = 'IN'
    CURRENT = 'CU'
    ARCHIVE = 'AR'
    status_choices = [
        (INBOX, 'Inbox'),
        (CURRENT, 'Current'),
        (ARCHIVE, 'Archive'),
    ]

    creation_date = models.DateTimeField(
        auto_now_add=True
        )
    description = models.CharField(
        max_length=500
        )
    status = models.CharField(
        max_length=2, 
        choices=status_choices, 
        default=INBOX
        )
    job_address = models.ForeignKey(
        Address, on_delete=models.CASCADE, related_name="job_address"
        )
    billing_address =  models.ForeignKey(
        Address, on_delete=models.CASCADE, related_name="billing_address"
        )

    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="client"
        )
    

    def __str__(self):
        return
    
    def client_name(self):
        return self.first + " " + self.last