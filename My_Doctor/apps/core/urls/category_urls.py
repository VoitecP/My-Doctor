from django.urls import path

from ..views import category_views
from ..views.category_views import *

urlpatterns =[
    path('list/', CategoryListView.as_view(), name='category-list'),
    # path('<uuid:pk>/',category_views.CategoryAPIView.as_view(), name='instance-category-view'),
    
    ]

