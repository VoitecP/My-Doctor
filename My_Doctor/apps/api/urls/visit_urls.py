from ..views import visit_views
from rest_framework.routers import DefaultRouter 
from django.urls import path, include 

router=DefaultRouter()
router.register(r'visits', visit_views.VisitListView, basename='viewsets-visits')



urlpatterns =[
    path('',include(router.urls)),
    # path('patients/<str:pk>/',PatientApi.as_view(),name='views-patient'),
    # path('doctors/', DoctorsApi.as_view(),name='views-doctors'),
    # path('doctors/<str:pk>/', DoctorApi.as_view(),name='views-doctor'),
    # path('categories/', CategoriesApi.as_view(),name='views-categories'),
    # path('categories/<str:pk>/', CategoryApi.as_view(),name='views-category'),
    # path('visits/', VisitsApi.as_view(),name='views-visits'),
    # path('visits/<str:pk>/', VisitApi.as_view(),name='views-visit'),  
]



