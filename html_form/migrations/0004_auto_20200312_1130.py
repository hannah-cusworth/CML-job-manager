# Generated by Django 3.0.3 on 2020-03-12 11:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('html_form', '0003_auto_20200311_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='email',
            field=models.EmailField(max_length=64, validators=[django.core.validators.EmailValidator()]),
        ),
    ]
