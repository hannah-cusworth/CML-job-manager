# Generated by Django 3.0.3 on 2020-03-13 15:49

from django.db import migrations, models
import html_form.validators


class Migration(migrations.Migration):

    dependencies = [
        ('html_form', '0006_auto_20200312_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='email',
            field=models.EmailField(max_length=64),
        ),
        migrations.AlterField(
            model_name='client',
            name='first',
            field=models.CharField(max_length=64, validators=[html_form.validators.validate_alpha]),
        ),
        migrations.AlterField(
            model_name='client',
            name='last',
            field=models.CharField(max_length=64, validators=[html_form.validators.validate_alpha]),
        ),
    ]
