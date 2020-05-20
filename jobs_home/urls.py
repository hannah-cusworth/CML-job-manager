from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'jobs_home'

urlpatterns = [

    path("", views.CurrentView.as_view(), name='current'),
    path("inbox", views.InboxView.as_view(), name='inbox'),
    path("archive", views.ArchiveView.as_view(), name='archive'),
    path("job/<int:job_id>", views.JobView.as_view(), name='jobs'),
    path("client/<int:client_id>", views.ClientView.as_view(), name='clients'),
    path("address/<int:address_id>", views.AddressView.as_view(), name='address'),
    path("login", views.LoginView.as_view(), name='login'),
    path("logout", views.logout_view, name='logout'),

]