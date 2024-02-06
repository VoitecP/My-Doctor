from django import forms
from django.core import validators
from django.contrib.auth.forms import UserCreationForm
from ..models import User, Director, Patient

from django.contrib.auth.forms import AuthenticationForm
from django.forms.models import inlineformset_factory

from .user_forms import UserForm

class PatientForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = ['phone', 'birth_date', 'adress' ]



# class PatientUpdateForm(forms.ModelForm):

#     user_data = UserForm()


#     class Meta:
#         model = Patient
#         fields = ['phone', 'birth_date', 'adress', 'user_data', 'birth_date', ]


#     def __init__(self, *args, **kwargs):
#         user_data = kwargs.pop('user_data', None)  # Pobranie niestandardowych danych
#         super().__init__(*args, **kwargs)

#         if user_data:
#             # Ustawienie początkowych danych dla formularza UserForm
#             self.fields['user_data'].initial = user_data
#             # Ustawienie atrybutu widgetu na HiddenInput dla pola 'user'
#             self.fields['user_data'].widget = forms.HiddenInput()

#     def save(self, commit=True):
#         #user = self.cleaned_data.pop('user_data')
#         patient = super().save(commit=False)
#         patient.user.first_name = user['first_name']
#         patient.user.last_name = user['last_name']
#         patient.user.email = user['email']
#         if commit:
#             patient.user.save()
#             patient.save()
#         # return patient

#         return super().save(commit=commit)



# PatientFormset = inlineformset_factory(
#     Patient, User, fields = ('username', 'first_name', 'last_name','email', 'adress')
# )