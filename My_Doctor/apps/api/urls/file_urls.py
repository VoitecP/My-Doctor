from ..views import file_views
from rest_framework.routers import DefaultRouter 
from django.urls import path, include 


router=DefaultRouter()
router.register(r'files', file_views.PatientPhotoListView, basename='viewsets-files')

urlpatterns =[
    path('',include(router.urls)),
    path('upload/',file_views.PatientPhotoCreateView.as_view(), name='patient-photo-create'), 
]
