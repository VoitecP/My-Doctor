from ..views import patient_views
from rest_framework.routers import DefaultRouter 
from django.urls import path, include 


router=DefaultRouter()
router.register(r'patients', patient_views.PatientViewset, basename='patients')


urlpatterns =[
    path('',include(router.urls)),
 
]

