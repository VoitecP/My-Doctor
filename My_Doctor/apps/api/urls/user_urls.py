from django.urls import path

from ..views import user_views
from ..views.user_views import *


urlpatterns =[
    path('', UserListCreateView.as_view(), name='list-user-view'),
    path('<uuid:pk>/',UserAPIView.as_view(), name='instance-user-view'),
    ##
    path('register/',user_views.UserRegisterView.as_view(), name='user-register'),
    path('user/<uuid:pk>/type-create/',user_views.UserTypeCreateView.as_view(), name='user-type-update'),
    path('user/<uuid:pk>/type-update/',user_views.UserTypeUpdateView.as_view(), name='user-profile-update'),
    path('user/<uuid:pk>/user-update/', user_views.UserUpdateView.as_view(), name='user-update'),
    path('user/<uuid:pk>/user-pernament-delete/', user_views.UserPernamentDeleteView.as_view(), name='user-pernament-delete'),
    path('user/<uuid:pk>/user-delete/',user_views.UserDeleteView.as_view(), name='user-delete'),
    
    ]


 # http://127.0.0.1:8000/api/user/login/
 # http://127.0.0.1:8000/api/user/logout/





