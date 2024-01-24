from django.urls import path

from ..views import category_views


urlpatterns =[
    path('', category_views.CategoryListCreateView.as_view(), name='list-category-view'),
    path('<uuid:pk>/',category_views.CategoryAPIView.as_view(), name='instance-category-view'),
    ]


