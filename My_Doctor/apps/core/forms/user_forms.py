from django import forms
from django.core import validators
from django.contrib.auth.forms import UserCreationForm
from ..models import User, Director

from django.contrib.auth.forms import AuthenticationForm


class UserCreateForm(UserCreationForm):

    usertype = forms.ChoiceField(label='User Type', choices=[])

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'usertype']

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['usertype'].choices = self.get_usertype_choices()


    def get_usertype_choices(self):
        choices = {
            'p': 'Patient',
            'd': 'Doctor',
            'c': 'Director',
        }
        if Director.objects.exists():
            choices.pop('c')
        return choices.items()

    




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
    


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name','email']

       
        