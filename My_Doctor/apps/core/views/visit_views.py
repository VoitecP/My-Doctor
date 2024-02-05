from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from apps.core.models import Visit


class VisitView(LoginRequiredMixin, ListView):

    model = Visit
    template_name = 'user/profile.html'  
    context_object_name = 'visits'  
    queryset = Visit.objects.all() 
    
    paginate_by = 6  # Określenie liczby obiektów na stronie, jeśli chcesz paginację
    # ordering = ['-date']  # Określenie kolejności obiektów

    # Opcjonalne metody, które można przesłonić, aby dostosować zachowanie widoku ListView:
    # def get_queryset(self):
    #     return Visit.objects.filter(status='active')
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['additional_data'] = AdditionalData.objects.all()
    #     return context




# class UserLoginView(LoginView):

#     # form_class = 
#     template_name = 'user/login.html'  # Ścieżka do szablonu logowania
#     success_url = reverse_lazy('home')


    

# class UserLoginView(LoginView):

#     # form_class = 
#     template_name = 'user/login.html' 
#     success_url = reverse_lazy('home')


# class UserLogoutView(View):

#     def get(self,request):
#         logout(request)
#         messages.success(request,("You are logged out"))
#         return redirect('apps.core:base')