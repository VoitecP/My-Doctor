from django.urls import path, include 
from rest_framework.routers import DefaultRouter

from ..views import (
    CategoryViewSet , DirectorViewSet, DoctorViewSet,
    VisitImageViewSet,PatientViewSet, PatientImageViewSet, 
    UserViewSet, VisitViewSet
                     )


router=DefaultRouter()

router.register(r'visit', VisitViewSet, basename='visit')
router.register(r'category',  CategoryViewSet, basename='category')
router.register(r'director', DirectorViewSet, basename='director')
router.register(r'doctor', DoctorViewSet, basename='doctor')
router.register(r'patient', PatientViewSet, basename='patient')
router.register(r'image', VisitImageViewSet, basename='image')
router.register(r'user', UserViewSet, basename='user')


# app_name='apps.api'
app_name='api' 

urlpatterns =[
    path('',include(router.urls)),
    ]

