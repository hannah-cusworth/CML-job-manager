from django.urls import path
from html_form.views import FormView


app_name = 'html_form'

urlpatterns = [
    
    path('new/', FormView.as_view(), name='new'),

]