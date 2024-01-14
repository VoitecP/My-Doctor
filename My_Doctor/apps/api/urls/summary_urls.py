from django.urls import path

from ..views import summary_views


urlpatterns =[
    path('viewset/summary-year/', summary_views.SummaryYearVisitListView.as_view({'get': 'list'}), name='summary-year'),  
    path('viewset/summary-month/', summary_views.SummaryMonthVisitListView.as_view({'get': 'list'}), name='summary-month'),  
    path('viewset/summary-category/', summary_views.SummaryCategoryVisitListView.as_view({'get': 'list'}), name='summary-category'),  
    path('viewset/summary-doctor/', summary_views.SummaryYearVisitListView.as_view({'get': 'list'}), name='summary-doctor'),  
    path('view/summary-total/',summary_views.SummaryVisitView.as_view(), name='summary-total'),
    ]
