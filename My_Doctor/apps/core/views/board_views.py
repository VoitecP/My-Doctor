# from django.views.generic import DetailView
# from django.views.generic.base import View
from django.urls import reverse_lazy

# from django import views
from django.views import View
from django.views.generic import TemplateView, CreateView, UpdateView
# from django.http import HttpResponse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic.list import ListView

from apps.core.models import Category, Visit, User

from apps.core.forms import UserCreateForm, ProfileUpdateForm
from apps.core.permissions import UpdatedRequiredMixin


class LoginWelcome(LoginView):

    template_name = 'forms/login.html'
    redirect_authenticated_user = True
    #success_url = reverse_lazy('apps.core:profile-view')


class RegisterWelcome(CreateView):

    template_name = 'forms/register.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('apps.core:welcome-login') 


class LogoutView(View):

    def get(self,request):
        logout(request)
        messages.success(request,("You are logged out"))
        # return redirect('apps.core:login')
        return redirect(reverse_lazy('apps.core:welcome-login'))
    


class Board2View(LoginRequiredMixin, ListView):

    model = Visit
    template_name = 'board/board.html'  
    context_object_name = 'visits'  
    queryset = Visit.objects.all() 
    
    paginate_by = 6  # Określenie liczby obiektów na stronie, jeśli chcesz paginację
    # ordering = ['-date']  # Określenie kolejności obiektów



# class BoardView(LoginRequiredMixin, UpdatedRequiredMixin, TemplateView):
class BoardView(LoginRequiredMixin, TemplateView):

    model = Visit
    template_name = 'board/board.html'  
    context_object_name = 'visits'  
    queryset = Visit.objects.all() 
    
    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context['user_pk'] = self.request.user.pk
        if user.is_staff == True:
            context['type_updated'] = True
        else:
            # context['type_updated'] = getattr(user, 'type_updated', False)
            context['type_updated'] = False

        return context

    # paginate_by = 6  
    # ordering = ['-date'] 



class ProfileUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    template_name = 'board/board_update.html'  
    context_object_name = 'users'  
    form_class = ProfileUpdateForm
    success_url = '/'   


    def form_valid(self, form):
        messages.success(self.request,("Profile updated"))
        return super().form_valid(form)
    
    # def get_context_data(self, **kwargs):
    #     user = self.request.user
    #     context = super().get_context_data(**kwargs)
    #     if user.is_staff:
    #         context['is_updated'] = False
    #     else:
    #         context['is_updated'] =  getattr(user, 'is_updated', False)
    #         context['form'] = ProfileUpdateForm()
    #     return context

    # paginate_by = 6  
    # # ordering = ['-date'] 