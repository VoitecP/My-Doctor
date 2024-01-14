from django.urls import path

from ..views import director_views


urlpatterns =[
    path('create/',director_views.DirectorCreateView.as_view(), name='director-create'),
   ]