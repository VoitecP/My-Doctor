from django.urls import path

from ..views import director_views 


urlpatterns =[
    path('', director_views.DirectorListCreateView.as_view(), name='list-dicrector-view'),
    path('<uuid:pk>/', director_views.DirectorAPIView.as_view(), name='instance-director-view'),
   ]