from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from apps.core.models import Visit


class VisitListView(LoginRequiredMixin, ListView):

    model = Visit
    # template_name = 'endpoints/visit/visit_list.html'
    template_name = 'base/board.html'    
    context_object_name = 'visits'   
    paginate_by = 6  
    # ordering = ['-date']  

   
    def get_queryset(self):
        user = self.request.user
        return Visit.objects.filter(patient__user=user)
        # return Visit.objects.all()
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['additional_data'] = AdditionalData.objects.all()
    #     return context


    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context['user_pk'] = user.pk
        context['panel'] = 'panel_patient/visit_list.html'
        if user.is_staff:
            context['type_updated'] = True
        else:
            context['type_updated'] = getattr(user, 'type_updated', False)
            # context['type_updated'] = False
        return context
