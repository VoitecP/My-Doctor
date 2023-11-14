from ..views import visit_views
from rest_framework.routers import DefaultRouter 
from django.urls import path, include 

router=DefaultRouter()
router.register(r'visit', visit_views.VisitListView, basename='viewsets-visits')



urlpatterns =[
    path('',include(router.urls)),
    # path('create/',visit_views.VisitCreateView.as_view(),name='create-visit'),
    # path('create/',visit_views.VisitCreateView.as_view(),name='create-visit'),

    # path('visits/<uuid:pk>/update/',visit_views.VisitUpdateView.as_view(),name='visit-update'),
    # path('visits/<uuid:pk>/delete/',visit_views.VisitDeleteView.as_view(),name='visit-delete'),
    
    
    
]




# urlpatterns =[
#     path('', include(router.urls)),   
         
#     path('register/',user_views.UserRegisterView.as_view(), name='user-register'),
#     path('user/<uuid:pk>/type-create/',user_views.UserTypeCreateView.as_view(), name='user-type-update'),
#     path('user/<uuid:pk>/type-update/',user_views.UserTypeUpdateView.as_view(), name='user-profile-update'),
#     path('user/<uuid:pk>/user-update/', user_views.UserUpdateView.as_view(), name='user-update'),
#     path('user/<uuid:pk>/user-pernament-delete/', user_views.UserPernamentDeleteView.as_view(), name='user-pernament-delete'),
#     path('user/<uuid:pk>/user-delete/',user_views.UserDeleteView.as_view(), name='user-delete'),
    
# ]
