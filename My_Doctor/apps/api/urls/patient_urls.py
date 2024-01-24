from django.urls import path

from ..views import patient_views


urlpatterns =[
    path('', patient_views.PatientListCreateView.as_view(), name='list-patient-view'),
    path('<uuid:pk>/', patient_views.PatientAPIView.as_view(), name='instance-patient-view'),
    ]
    
