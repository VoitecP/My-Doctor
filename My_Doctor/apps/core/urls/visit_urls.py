from django.urls import path
from django.contrib.auth.views import LogoutView

from ..views import category_views
from ..views.visit_views import *


urlpatterns =[
    path('visits/', VisitView.as_view(), name='visit-list'),


    # path('login/', UserLoginView.as_view(), name='user-login'),
    # path('logout/', UserLogoutView.as_view(), name='user-logout')
    # path('<uuid:pk>/',category_views.CategoryAPIView.as_view(), name='instance-category-view'),
    
    ]

