from django.urls import path

from ..views.user_views import *


urlpatterns =[
    path('', UserListCreateView.as_view(), name='list-user-view'),
    path('<uuid:pk>/',UserAPIView.as_view(), name='instance-user-view'),
    ##
    path('register/', UserCreateAPIView.as_view(), name='user-register'),
    path('register2/', UserRegisterView.as_view(), name='user-register2'),
    path('<uuid:pk>/update/', UserUpdateAPIView.as_view(), name='user-update'),
    path('<uuid:pk>/delete/', UserDestroyAPIView.as_view(), name='user-delete'),
    path('<uuid:pk>/pernament-delete/', UserPernamentDeleteView.as_view(), name='user-pernament-delete'),
    
    
    ]


 # http://127.0.0.1:8000/api/user/login/
 # http://127.0.0.1:8000/api/user/logout/





