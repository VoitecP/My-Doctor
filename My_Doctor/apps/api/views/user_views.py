from django.contrib.auth import login, logout
from rest_framework.permissions import IsAuthenticated, AllowAny 

from ..serializers import (UserDynamicSerializer, 
                           UserManageDynamicSerializer)
from ..permissions import UserPermissions
from ..views.view_mixins  import (ContextAPIView, ContextDestroyAPIView,
                     ContextCreateAPIView, ContextUpdateAPIView, 
                     ContextListCreateAPIView, ContextModelViewSet) 
from apps.core.models import User


class UserMixin:

    permission_classes=[IsAuthenticated, UserPermissions]
    serializer_class = UserDynamicSerializer

    def get_queryset(self):
        user=self.request.user
        if user.usertype in ['p','d']:
            return User.objects.filter(id=user.id)
        elif (user.usertype == 'c' or user.is_staff):
            return User.objects.all()
        return User.objects.none()


class UserViewSet(UserMixin, ContextModelViewSet):
    """
    User model List View (filtered list view)
    """
    pass

class UserListCreateView(UserMixin, ContextListCreateAPIView):
    """
    """
    pass


class UserAPIView(UserMixin, ContextAPIView):
    """
    """
    pass

    
class UserCreateAPIView(ContextCreateAPIView):

    permission_classes = [AllowAny]
    serializer_class  = UserManageDynamicSerializer
    queryset = User.objects.none()

    def perform_create(self, serializer):
        user = serializer.save()
        login(self.request, user)

    
class UserUpdateAPIView(ContextUpdateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = UserManageDynamicSerializer

    def get_queryset(self):
            user=self.request.user
            return User.objects.filter(id=user.id)


class UserDestroyAPIView(ContextDestroyAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = UserManageDynamicSerializer

    def get_queryset(self):
            user=self.request.user
            return User.objects.filter(id=user.id)


    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
        logout(self.request)

    
class UserPernamentDestroyAPIView(UserDestroyAPIView):

    def perform_destroy(self, instance):
        instance.delete()
        logout(self.request)
        
        


       




