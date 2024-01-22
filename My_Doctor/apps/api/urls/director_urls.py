from django.urls import path

from ..views.director_views import *


urlpatterns =[
    path('', DirectorListCreateView.as_view(), name='list-dicrector-view'),
    path('<uuid:pk>/',DirectorAPIView.as_view(), name='instance-director-view'),
   ]