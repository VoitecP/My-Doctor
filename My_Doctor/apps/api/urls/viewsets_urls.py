
from ..views.category_views import CategoryViewset
from ..views.director_views import DirectorViewset
from ..views.doctor_views import DoctorViewSet
from ..views.patient_views import PatientViewset
from ..views.file_views import PatientImageViewset
from ..views.user_views import UserViewSet


from django.urls import path, include 
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register(r'category',  CategoryViewset, basename='category')
router.register(r'director', DirectorViewset, basename='director')
router.register(r'doctor', DoctorViewSet, basename='doctor')
router.register(r'patient', PatientViewset, basename='patient')
router.register(r'image', PatientImageViewset, basename='image')
router.register(r'user', UserViewSet, basename='user')



app_name='api'
urlpatterns =[
    path('',include(router.urls)),

]
