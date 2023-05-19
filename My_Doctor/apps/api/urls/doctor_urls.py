from ..views import doctor_views
from rest_framework.routers import DefaultRouter 
from django.urls import path, include 


router=DefaultRouter()
router.register(r'doctors', doctor_views.DoctorListView, basename='viewsets-doctors')

urlpatterns =[
    path('',include(router.urls)),
 
]
