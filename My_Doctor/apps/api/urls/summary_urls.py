from ..views import summary_views

from rest_framework.routers import DefaultRouter 
from django.urls import path, include 

# TODO # Replace from router to as.view.

router=DefaultRouter()
router.register(r'year', summary_views.SummaryYearVisitListView, basename='viewsets-year-summary')
router.register(r'month', summary_views.SummaryMonthVisitListView, basename='viewsets-month-summary')
router.register(r'category', summary_views.SummaryCategoryVisitListView, basename='viewsets-category-summary')
router.register(r'doctor', summary_views.SummaryDoctorVisitListView, basename='viewsets-doctor-summary')
#router.register(r'total', summary_views.SummaryVisitView, basename='total')


urlpatterns =[
    path('', include(router.urls)),
    path('year-view/', summary_views.SummaryYearVisitListView.as_view({'get': 'list'}), name='sumary-list'),  
    path('total/',summary_views.SummaryVisitView.as_view(), name='visit-total'),
]




# TotalSumVisitListView
