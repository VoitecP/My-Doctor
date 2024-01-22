from django.urls import path

from ..views.category_views import *


urlpatterns =[
    path('', CategoryListCreateView.as_view(), name='list-category-view'),
    path('<uuid:pk>/',CategoryAPIView.as_view(), name='instance-category-view'),
    # path('create/',category_views.CategoryCreateView.as_view(), name='category-create'),
    # path('category/<uuid:pk>/update/',category_views.CategoryUpdateView.as_view(), name='category-update'),
    # path('category/<uuid:pk>/delete/',category_views.CategoryDeleteView.as_view(), name='category-delete'),
    ]


