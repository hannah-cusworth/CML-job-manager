# Generated by Django 3.0.3 on 2020-03-11 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('html_form', '0003_auto_20200311_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='first',
            field=models.CharField(max_length=2),
        ),
    ]
