from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView,  TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from apps.core.models import Visit, VisitImageFile


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



class VisitDetailView(LoginRequiredMixin, DetailView):

    model = Visit
    template_name = 'base/board.html'    
    context_object_name = 'visit'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        visit = self.get_object()
        images = visit.visit_image.all()  
        context['images'] = images 
        context['user_pk'] = user.pk
        context['panel'] = 'panel_patient/visit_detail.html'
        return context
    


class VisitDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    
    model = Visit
    success_url = reverse_lazy('apps.core:patient-visit-list')
    template_name = 'base/board.html'
    # message = 'Visit successfully deleted'
    success_message = 'Visit successfully deleted'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['user_pk'] = visit.pk
        context['panel'] = 'panel_patient/visit_delete.html'
        return context
    
    # def delete(self, request, *args, **kwargs):
    #     messages.success(self.request, self.message)  
    #     return super().delete(request, *args, **kwargs)