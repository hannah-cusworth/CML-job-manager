# Generated by Django 3.0.3 on 2020-03-12 11:42

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('html_form', '0004_auto_20200312_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='number',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None),
        ),
    ]
