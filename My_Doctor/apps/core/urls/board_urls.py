from django.urls import path

from ..views import category_views
from ..views.board_views import *

urlpatterns =[
    path('', BoardView.as_view(), name='boardview'),
    path('register/', RegisterWelcome.as_view(), name='welcome-register'),
    path('login/', LoginWelcome.as_view(), name='welcome-login'),
    path('logout/', LogoutView.as_view(), name='user-logout'),
    path('<uuid:pk>/update/', ProfileUpdateView.as_view(), name='profile-update')

    # path('<uuid:pk>/',category_views.CategoryAPIView.as_view(), name='instance-category-view'),
    
    ]

