from django.contrib.auth import login, logout, authenticate
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveDestroyAPIView,UpdateAPIView, CreateAPIView, ListCreateAPIView
from rest_framework.response import Response 
from rest_framework.serializers import ValidationError
from rest_framework.viewsets import GenericViewSet,  ReadOnlyModelViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from ..serializers import user_serializers
from ..permissions import IsDoctorCreated, IsPatientCreated, IsNotUserUpdated, UserPermissions
from ..permissions import *
from .view_mixins import UserQuerysetMixin, UserObjectMixin, UserSerializerMixin
from .view_mixins import ContextModelViewSet
from apps.core.models import User


class UserViewSet(ContextModelViewSet):
    """
    User model List View (filtered list view)
    """

    serializer_class = user_serializers.UserDynamicSerializer
    # permission_classes=[IsAuthenticated, UserPermissions]
            
    def get_queryset(self):
        user=self.request.user

        if user.usertype == 'p':
            return User.objects.filter(id=user.id)
        if user.usertype == 'd':
            return User.objects.filter(id=user.id)
        if user.usertype == 'c' or user.is_staff:
            return User.objects.all()


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
    permission_classes=[IsAuthenticated, IsAdminUser]
        
    def get_serializer_class(self):
        return user_serializers.UserUpdateSerializer

    # def path(self, request, *args, **kwargs):
    #     return self.partial_update(request, *args, **kwargs)


class UserTypeCreateView(UserQuerysetMixin, UserSerializerMixin, ListCreateAPIView):
    """
    View for create Patient/Doctor/Director model
    """
    # TODO: When Usertype is created in signals, (later should be confirmed by email,
    # TODO: User should be redirect or blocked ; to be only able to update profile
    # This view is not need, onle user type update view
    permission_classes = [IsAuthenticated, IsNotUserUpdated] #, IsAdminUser]   it can make errors

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
            return Response({"detail": "Success"})
        except:
            raise ValidationError({"detail": "Operation not allowed"})
        
    
class UserTypeUpdateView(UserObjectMixin, UserSerializerMixin,  RetrieveUpdateAPIView): 
    """
    View for Update Patient/Doctor/Director model
    """
    permission_classes = [IsAuthenticated, IsUserUpdated]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


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
