from django.urls import path

from . import views

app_name = 'html_form'

urlpatterns = [

    path("form/", views.index, name='form')

]