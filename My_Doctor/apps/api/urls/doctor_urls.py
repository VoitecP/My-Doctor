from django.urls import path
from ..views.doctor_views import *


urlpatterns = [
    path('', DoctorListCreateView.as_view(), name='list-doctor-view'),
    path('<uuid:pk>/',DoctorAPIView.as_view(), name='instance-doctor-view'),
    ]