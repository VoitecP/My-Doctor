# from django.views.generic import DetailView
# from django.views.generic.base import View
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
# from django import views
from django.views import View
from django.views.generic import TemplateView, CreateView, UpdateView
# from django.http import HttpResponse
from django.contrib.auth.views import LoginView, LogoutView as BaseLogoutView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic.list import ListView

from apps.core.models import Category, Visit, User, Patient

from apps.core.forms import UserCreateForm, ProfileUpdateForm, PatientForm, UserForm
from apps.core.permissions import UpdatedRequiredMixin




class RegisterWelcome(CreateView):

    template_name = 'base/forms/register.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('apps.core:welcome-login') 


class LoginWelcome(LoginView):

    template_name = 'base/forms/login.html'
    redirect_authenticated_user = True
    #success_url = reverse_lazy('apps.core:profile-view')


class LogoutView(BaseLogoutView):

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.success(request, "You are logged out.")
        return response
    

class Board2View(LoginRequiredMixin, ListView):

    model = Visit
    template_name = 'board/board.html'  
    context_object_name = 'visits'  
    queryset = Visit.objects.all() 
    
    paginate_by = 6  
    # ordering = ['-date']  


class BoardView(LoginRequiredMixin, TemplateView):

    template_name = 'base/board.html'  

    def get_panel(self):
        user = self.request.user
        if user.type_updated or user.is_staff:
            if user.usertype == 'p':
                panel = 'panel_patient/panel.html'
            elif user.usertype == 'd':
                panel = 'panel_doctor/panel.html'
            elif user.usertype == 'c' or user.is_staff:
                panel = 'panel_director/panel.html'
        else:
            panel = 'base/panel_profile_update.html'
        return panel
    

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context['user_pk'] = user.pk
        context['panel'] = self.get_panel
        if user.is_staff:
            context['type_updated'] = True
        else:
            context['type_updated'] = getattr(user, 'type_updated', False)
            # context['type_updated'] = False
        return context



class ProfileUpdateView(LoginRequiredMixin, UpdateView):

    model = Patient
    template_name = 'base/board.html'  
    context_object_name = 'patient'  

    form_class = PatientForm
    user_form_class = UserForm
    success_url = '/'   


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['panel'] = 'base/forms/profile_update.html'
        context['form'] =  self.form_class(instance=self.get_object())
        context['user_form'] = self.user_form_class(instance=self.get_object().user)
        return context


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)
        user_form = self.user_form_class(request.POST, instance=self.object.user)

        if form.is_valid() and user_form.is_valid():
            user = user_form.save()
            patient = form.save(commit=False)
            patient.user = user
            patient.save()
            messages.success(self.request, 'Profile update successfully')
            return HttpResponseRedirect(self.success_url)
           
        return self.render_to_response(
                self.get_context_data(form=form, user_form=user_form))


