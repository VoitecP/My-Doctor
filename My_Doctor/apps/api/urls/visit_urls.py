from django.urls import path

from ..views.visit_views import *

# app_name='apps.api'
# app_name='api' 


urlpatterns =[ 
    path('', VisitListCreateView.as_view(), name='list-visit-view'),
    path('<uuid:pk>/',VisitAPIView.as_view(), name='instance-visit-view'),
    ]


