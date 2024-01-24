from django.urls import path

from ..views.user_views import *


urlpatterns =[
    path('', UserListCreateView.as_view(), name='list-user-view'),
    path('<uuid:pk>/', UserAPIView.as_view(), name='instance-user-view'),
    #
    path('register/', UserCreateAPIView.as_view(), name='user-register'),
    path('<uuid:pk>/update/', UserUpdateAPIView.as_view(), name='user-update'),
    path('<uuid:pk>/delete/', UserDestroyAPIView.as_view(), name='user-delete'),
    path('<uuid:pk>/pernament-delete/', UserPernamentDestroyAPIView.as_view(), name='user-pernament-delete'),
    ]


