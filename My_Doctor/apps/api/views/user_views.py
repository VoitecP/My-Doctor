from django.contrib.auth import login, logout, authenticate
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveDestroyAPIView,UpdateAPIView, CreateAPIView, ListCreateAPIView
from rest_framework.response import Response 
from rest_framework.serializers import ValidationError
from rest_framework.viewsets import GenericViewSet,  ReadOnlyModelViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny 
from rest_framework.generics import  ListCreateAPIView, RetrieveUpdateDestroyAPIView

from ..serializers import user_serializers
from ..serializers.user_serializers import UserDynamicSerializer, UserManageDynamicSerializer
# from ..permissions import IsDoctorCreated, IsPatientCreated, IsNotUserUpdated, UserPermissions
from ..permissions import *
from .view_mixins import ContextMixin, UserQuerysetMixin, UserObjectMixin, UserSerializerMixin
from .view_mixins import (ContextCreateAPIView, ContextUpdateAPIView, ContextListCreateAPIView, 
                          ContextAPIView, ContextModelViewSet, ContextDestroyAPIView) 
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


class UserAuthView(GenericViewSet):
    """
    View for User Login, Logout
    """
    permission_classes = [AllowAny]
    serializer_class=user_serializers.LoginUserSerializer

    @action(detail=False, methods=["post"], url_path='login')  
    def user_login(self, request):                             
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password'],
            )
            if user  is not None :
                login(request, user)
                return Response({"Successfully logged in": request.user.username}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "You are not logged in"}, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=["GET"], url_path='logout')
    def user_logout(self, request):
        if request.user.is_authenticated == False:
            return Response({"detail": "You are not logged in"}, status=status.HTTP_400_BAD_REQUEST)
        logout(request)
        return Response({"detail": "Successfully logged out"}, status=status.HTTP_200_OK)
    

class UserRegisterView(CreateAPIView):
    """
    User register View
    """
    # TODO  Automatic Logout if user is loged in.  
    permission_classes = [AllowAny]

    def get_queryset(self):
        return User.objects.none()
       
    def get_serializer_class(self):
        return user_serializers.UserRegisterSerializer
        
    def perform_create(self, serializer):
        try:
            serializer.save()
            return Response({"detail": "Success"})
        except:
            raise ValidationError({"detail": "Operation not allowed"})

       


class UserUpdateView(UserObjectMixin, RetrieveUpdateAPIView):
    """
    View for update User model
    """
    permission_classes=[IsAuthenticated]
        
    def get_serializer_class(self):
        return user_serializers.UserUpdateSerializer

    # def path(self, request, *args, **kwargs):
    #     return self.partial_update(request, *args, **kwargs)


        
    



class UserPernamentDeleteView(UserSerializerMixin, UserObjectMixin, RetrieveDestroyAPIView): 
    """
    View for pernament delete User model
    """
    permission_classes = [IsAuthenticated]
    
    def destroy(self, request, *args, **kwargs):
        try:
            user = request.user
            user.delete()
            logout(request)
            return Response({"detail": "User deleted pernamently"})
        except:
            return Response({"detail": "User Cannot be deleted"})


class UserDeleteView(UserSerializerMixin, UserObjectMixin, RetrieveDestroyAPIView): 
    """
    View for deleting (making inactive) User model
    """
    permission_classes = [IsAuthenticated]
    
    def destroy(self, request, *args, **kwargs):
        try:
            user = request.user
            user.is_active = False
            user.save()
            logout(request)
            return Response({"detail": "User has status 'inactive' "})
        except:
            return Response({"detail": "Cannot set status 'inactive' "})

# for director only  all users
# for p , d  only  self.id
