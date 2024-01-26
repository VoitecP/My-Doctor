from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views import View

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


class UserLoginView(LoginView):

    # form_class = 
    template_name = 'user/login.html'  # Ścieżka do szablonu logowania
    success_url = reverse_lazy('home')


# class LoginUserView(LoginView):
#     redirect_authenticated_user = True
#     template_name = 'users/login.html'

#     def get_success_url(self):
#         return reverse_lazy('home')

#     def form_valid(self, form):
#         valid = super(LoginUserView, self).form_valid(form)
#         username, password = form.cleaned_data.get(
#             'username'), form.cleaned_data.get('password1')
#         user = authenticate(username=username, password=password)
#         login(self.request, user)
#         return valid
    

class UserLoginView(LoginView):

    # form_class = 
    template_name = 'user/login.html' 
    success_url = reverse_lazy('home')


class UserLogoutView(View):

    def get(self,request):
        logout(request)
        messages.success(request,("You are logged out"))
        return redirect('apps.core:base')