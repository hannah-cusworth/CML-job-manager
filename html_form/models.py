from django.db import models
from datetime import datetime
from django.core.validators import validate_email
from phonenumber_field.modelfields import PhoneNumberField
from localflavor.gb.forms import GB_REGION_CHOICES
from .validators import validate_alpha

class Address(models.Model):
    address_type_choices = [
        ("BILL", 'Billing'),
        ("JOB", 'Job')
    ]

    client = models.ManyToManyField('Person', related_name="owner")
    line_one = models.CharField(max_length=64,)
    line_two = models.CharField(max_length=64, blank=True)
    city = models.CharField(max_length=64)
    county = models.CharField(
        max_length=64,
        choices=GB_REGION_CHOICES,
        )
    postcode = models.CharField(max_length=20)
    creation_date = models.DateTimeField(
        auto_now_add=True
        )
    address_type = models.CharField(
        default = "JOB",
        max_length = 4,
        choices = address_type_choices,
    )



class Person(models.Model):
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
    number = PhoneNumberField(max_length=20)
    creation_date = models.DateTimeField(
        auto_now_add=True
        )
    address = models.ManyToManyField(Address, related_name="address")


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
        Person, on_delete=models.CASCADE, related_name="client"
        )
    