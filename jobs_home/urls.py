from django.urls import path
from jobs_home.views import JobView, InboxView
from . import views

app_name = 'jobs_home'

urlpatterns = [

    path("", views.current, name='current'),
    path("inbox", InboxView.as_view(), name='inbox'),
    path("archive", views.archive, name='archive'),
    path("<int:job_id>", JobView.as_view(), name='jobs')

]