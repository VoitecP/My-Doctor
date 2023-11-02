from ..views import summary_views

from rest_framework.routers import DefaultRouter 
from django.urls import path, include 


router=DefaultRouter()
router.register(r'year', summary_views.SummaryYearVisitListView, basename='viewsets-year-summary')
router.register(r'month', summary_views.SummaryMonthVisitListView, basename='viewsets-month-summary')
router.register(r'category', summary_views.SummaryCategoryVisitListView, basename='viewsets-category-summary')

urlpatterns =[
    path('', include(router.urls)),   
         
    #path('register/',user_views.UserRegisterView.as_view(), name='user-register'),
]
