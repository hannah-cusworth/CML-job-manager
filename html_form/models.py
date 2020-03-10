from django.db import models



class Address(models.Model):
    client = models.ManyToManyField('Client', related_name="client")
    line_one = models.CharField(max_length=64)
    line_two = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    county = models.CharField(max_length=64)
    postcode = models.CharField(max_length=64)

    def __str__(self):
        return f"{client.first} {client.last}\n{self.line_one}\n{self.line_two}\n{self.city}\n{self.county}\n{self.postcode}"



class Client(models.Model):
    first = models.CharField(max_length=64)
    last = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    number = models.CharField(max_length=64)
    address = models.ManyToManyField(Address, related_name="address")

    def __str__(self):
        return f"{self.first.capitalize} {self.last.capitalize}\n{self.email}\n{self.number}\n{self.address}"


class Job(models.Model):
    INBOX = 'IN'
    CURRENT = 'CU'
    ARCHIVE = 'AR'
    status_choices = [
        (INBOX, 'Inbox'),
        (CURRENT, 'Current'),
        (ARCHIVE, 'Archive'),
    ]

    creation_date = models.DateTimeField
    description = models.CharField(max_length=500)
    status = models.CharField(max_length=2, choices=status_choices, default=INBOX)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return