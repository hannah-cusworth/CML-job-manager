from django.urls import path

from . import views

app_name = 'jobs_home'

urlpatterns = [

    path("", views.index, name='home')

]