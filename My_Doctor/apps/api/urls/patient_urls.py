from django.urls import path

from ..views.patient_views import *

urlpatterns =[
    path('', PatientListCreateView.as_view(), name='list-patient-view'),
    path('<uuid:pk>/',PatientAPIView.as_view(), name='instance-patient-view'),
    ]
    
