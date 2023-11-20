from ..views import category_views


from django.urls import path, include 

urlpatterns =[


    path('create/',category_views.CategoryCreateView.as_view(), name='category-create'),
    path('category/<uuid:pk>/update/',category_views.CategoryUpdateView.as_view(), name='category-update'),
    path('category/<uuid:pk>/delete/',category_views.CategoryDeleteView.as_view(), name='category-delete'),
    

]



# router=DefaultRouter()
# router.register(r'user', user_views.UserListView, basename='user-list')
# router.register('', user_views.UserAuthView, basename='login')           # Must be pattern  r''  not r'login' or 'login/'

# # router.register('type-update/',user_views.UserTypeUpdateView, basename='user-type-update'),

# urlpatterns =[
#     path('', include(router.urls)),   
         
#     path('user/register/',user_views.UserRegisterView.as_view(), name='user-register'),
#     path('user/<uuid:pk>/type-create/',user_views.UserTypeCreateView.as_view(), name='user-type-update'),
#     path('user/<uuid:pk>/type-update/',user_views.UserTypeUpdateView.as_view(), name='user-profile-update'),
#     path('user/<uuid:pk>/user-update/', user_views.UserUpdateView.as_view(), name='user-update'),
#     path('user/<uuid:pk>/user-pernament-delete/', user_views.UserPernamentDeleteView.as_view(), name='user-pernament-delete'),
#     path('user/<uuid:pk>/user-delete/',user_views.UserDeleteView.as_view(), name='user-delete'),
    
# ]