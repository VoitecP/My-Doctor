from django.urls import path

from ..views import file_views

urlpatterns =[
    path('', file_views.VisitImageListCreateView.as_view(), name='list-visitimage-view'),
    path('<uuid:pk>/', file_views.VisitImageAPIView.as_view(), name='instance-visitimage-view'),
    ]
