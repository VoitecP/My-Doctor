from ..views import user_views

from rest_framework.routers import DefaultRouter 
from django.urls import path, include 


# router=DefaultRouter()
# router.register(r'user', user_views.UserViewset, basename='viewsets-user')
# router.register('', user_views.UserAuthView, basename='login')           # Must be pattern  r''  not r'login' or 'login/'

# router.register('type-update/',user_views.UserTypeUpdateView, basename='user-type-update'),

#app_name='api'
urlpatterns =[
    # path('', include(router.urls)),   
         
    path('register/',user_views.UserRegisterView.as_view(), name='user-register'),
    path('user/<uuid:pk>/type-create/',user_views.UserTypeCreateView.as_view(), name='user-type-update'),
    path('user/<uuid:pk>/type-update/',user_views.UserTypeUpdateView.as_view(), name='user-profile-update'),
    path('user/<uuid:pk>/user-update/', user_views.UserUpdateView.as_view(), name='user-update'),
    path('user/<uuid:pk>/user-pernament-delete/', user_views.UserPernamentDeleteView.as_view(), name='user-pernament-delete'),
    path('user/<uuid:pk>/user-delete/',user_views.UserDeleteView.as_view(), name='user-delete'),
    
]


 # http://127.0.0.1:8000/api/user/login/
 # http://127.0.0.1:8000/api/user/logout/







