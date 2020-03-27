from django.urls import path
from jobs_home.views import *
from . import views

app_name = 'jobs_home'

urlpatterns = [

    path("", CurrentView.as_view(), name='current'),
    path("inbox", InboxView.as_view(), name='inbox'),
    path("archive", ArchiveView.as_view(), name='archive'),
    path("job/<int:job_id>", JobView.as_view(), name='jobs'),
    path("client/<int:client_id>", ClientView.as_view(), name='clients'),
    path("address/<int:address_id>", AddressView.as_view(), name='address'),


]