from django.urls import path

from ..views import category_views
from ..views.base_views import *

urlpatterns =[
    path('', BaseView.as_view(), name='base'),
    # path('<uuid:pk>/',category_views.CategoryAPIView.as_view(), name='instance-category-view'),
    
    ]

