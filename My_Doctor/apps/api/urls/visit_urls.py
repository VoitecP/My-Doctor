from django.urls import path

from ..views import visit_views 


urlpatterns =[ 
    path('', visit_views.VisitListCreateView.as_view(), name='list-visit-view'),
    path('<uuid:pk>/', visit_views.VisitAPIView.as_view(), name='instance-visit-view'),
    ]


