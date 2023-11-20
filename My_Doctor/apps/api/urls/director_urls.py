from ..views import director_views
from django.urls import path, include 
# from rest_framework.routers import DefaultRouter

# router=DefaultRouter()
# router.register(r'director', director_views.DirectorViewset, basename='director-list')

urlpatterns =[
    # path('',include(router.urls)),
    ## Disable create, or only for admin ##
    path('create/',director_views.DirectorCreateView.as_view(), name='director-create'),
    path('director/<uuid:pk>/update/',director_views.DirectorUpdateView.as_view(), name='director-update'),
    path('director/<uuid:pk>/delete/',director_views.DirectorDeleteView.as_view(), name='director-delete'),


]