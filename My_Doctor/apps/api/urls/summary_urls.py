from ..views import summary_views

from rest_framework.routers import DefaultRouter 
from django.urls import path, include 


# router=DefaultRouter()
# router.register(r'year', summary_views.SummaryYearVisitListView, basename='viewsets-year-summary')
# router.register(r'month', summary_views.SummaryMonthVisitListView, basename='viewsets-month-summary')
# router.register(r'category', summary_views.SummaryCategoryVisitListView, basename='viewsets-category-summary')
# router.register(r'doctor', summary_views.SummaryDoctorVisitListView, basename='viewsets-doctor-summary')
#router.register(r'total', summary_views.SummaryVisitView, basename='total')


urlpatterns =[
    # path('', include(router.urls)),
    path('viewset/summary-year/', summary_views.SummaryYearVisitListView.as_view({'get': 'list'}), name='summary-year'),  
    path('viewset/summary-month/', summary_views.SummaryMonthVisitListView.as_view({'get': 'list'}), name='summary-month'),  
    path('viewset/summary-category/', summary_views.SummaryCategoryVisitListView.as_view({'get': 'list'}), name='summary-category'),  
    path('viewset/summary-doctor/', summary_views.SummaryYearVisitListView.as_view({'get': 'list'}), name='summary-doctor'),  
    path('view/summary-total/',summary_views.SummaryVisitView.as_view(), name='summary-total'),
]




# TotalSumVisitListView
