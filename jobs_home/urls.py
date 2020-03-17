from django.urls import path
from jobs_home.views import JobView
from . import views

app_name = 'jobs_home'

urlpatterns = [

    path("", views.current, name='current'),
    path("inbox", views.inbox, name='inbox'),
    path("archive", views.archive, name='archive'),
    path("<int:job_id>", JobView.as_view(), name='jobs')

]