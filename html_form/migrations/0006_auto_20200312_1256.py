# Generated by Django 3.0.3 on 2020-03-12 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('html_form', '0005_auto_20200312_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='line_two',
            field=models.CharField(blank=True, max_length=64),
        ),
    ]
