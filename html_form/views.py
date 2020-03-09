from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse


def index(request):
        return render(request, "html_form/index.html")
   
class FormView(TemplateView):
    template_name = "html_form/form.html"