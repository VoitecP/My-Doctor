from ..views import user_views

from rest_framework.routers import DefaultRouter 
from django.urls import path, include 


router=DefaultRouter()
router.register(r'', user_views.LoginUserView, basename='user-login')           # Must be pattern  r''  not r'login' or 'login/'


urlpatterns =[
    path('', include(router.urls)),   
    # register error 'Userform serializer'          
    path('user-register/',user_views.RegisterUserView.as_view(),name='user-register'),
    # path('patients/<str:pk>/',PatientApi.as_view(),name='views-patient'),
    # path('doctors/', DoctorsApi.as_view(),name='views-doctors'),
    # path('doctors/<str:pk>/', DoctorApi.as_view(),name='views-doctor'),
    # path('categories/', CategoriesApi.as_view(),name='views-categories'),
    # path('categories/<str:pk>/', CategoryApi.as_view(),name='views-category'),
    # path('visits/', VisitsApi.as_view(),name='views-visits'),
    # path('visits/<str:pk>/', VisitApi.as_view(),name='views-visit'),  
]


 # http://127.0.0.1:8000/api/user/login/
 # http://127.0.0.1:8000/api/user/logout/







