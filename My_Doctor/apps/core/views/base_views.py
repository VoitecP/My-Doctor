# from django.views.generic import DetailView
# from django.views.generic.base import View

# from django import views
from django.views import View
from django.views.generic import TemplateView
# from django.http import HttpResponse


from django.views.generic.list import ListView

from apps.core.models import Category

class BaseView(TemplateView):
    
    template_name = 'base/base.html'
    