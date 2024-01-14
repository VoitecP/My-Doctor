from django.urls import path

from ..views import file_views


urlpatterns =[
    path('upload/',file_views.PatientImageCreateView.as_view(), name='patient-photo-create'), 
    ]
