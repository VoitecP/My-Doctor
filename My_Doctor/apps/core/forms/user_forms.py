from django import forms
from django.contrib.auth.forms import UserCreationForm
from ..models import User

from django.contrib.auth.forms import AuthenticationForm



class LoginUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, request, *args, **kwargs):
        super(LoginUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control',
                                                     "placeholder": "e.g. Luke"})
        self.fields['password'].widget.attrs.update({'class': 'form-control',
                                                      "placeholder": "Password"})
        




class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                    widget=forms.TextInput(attrs={'class': 'form-control', 
                                            'placeholder': 'Enter username'}))
    password = forms.CharField(label="Password", max_length=30, 
                    widget=forms.PasswordInput(attrs={'class': 'form-control', 
                                                      'placeholder': 'Enter password'}))