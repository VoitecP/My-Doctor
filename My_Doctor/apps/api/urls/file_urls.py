from django.urls import path

from ..views import file_views
from ..views.file_views import *


urlpatterns =[
    path('', VisitImageListCreateView.as_view(), name='list-visitimage-view'),
    path('<uuid:pk>/',VisitImageAPIView.as_view(), name='instance-visitimage-view'),
    #
    #path('upload/',file_views.PatientImageCreateView.as_view(), name='patient-photo-create'), 
    ]
