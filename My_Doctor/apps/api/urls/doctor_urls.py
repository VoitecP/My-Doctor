from ..views import doctor_views
from rest_framework.routers import DefaultRouter 
from django.urls import path, include 


router=DefaultRouter()
router.register(r'doctors', doctor_views.DoctorViewSet, basename='viewsets-doctors')

urlpatterns =[
    path('',include(router.urls)),
    # path('profile-update/',doctor_views.UserProfileUpdateView.as_view(), name='user-profile-update'), 
]
