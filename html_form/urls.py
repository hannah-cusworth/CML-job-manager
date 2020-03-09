from django.urls import path
from html_form.views import FormView
from . import views

app_name = 'html_form'

urlpatterns = [

    path("form/", views.index, name='form'),
    path('new/', FormView.as_view(), name='new'),

]