from django.urls import path

from ..views import doctor_views 


urlpatterns = [
    path('', doctor_views.DoctorListCreateView.as_view(), name='list-doctor-view'),
    path('<uuid:pk>/', doctor_views.DoctorAPIView.as_view(), name='instance-doctor-view'),
    ]