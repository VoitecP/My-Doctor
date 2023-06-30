from apps.core.models import User, Patient, Doctor, Director
from ..serializers import user_serializers
# from ..serializers.patient_serializers import PatientUpdateSerializer
# from ..serializers.doctor_serializers import DoctorUpdateSerializer
# from ..serializers.director_serializers import DirectorUpdateSerializer
from ..permissions import *
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, GenericViewSet,  ReadOnlyModelViewSet
from rest_framework.serializers import ValidationError

from django.contrib.auth import login, logout, authenticate
from rest_framework.response import Response  
from rest_framework.decorators import action

# from django.contrib.auth import logout as django_logout
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.generics import RetrieveUpdateAPIView, RetrieveDestroyAPIView,UpdateAPIView, CreateAPIView, ListCreateAPIView
from ..permissions import IsDoctorCreated, IsPatientCreated, IsNotUserUpdated

from django.shortcuts import get_object_or_404

from .mixins import QuerysetMixin, ObjectMixin, SerializerMixin


# class QuerysetMixin:

#     def get_queryset(self):
#         usertype=self.request.user.usertype
#         if usertype == 'p':
#             return Patient.objects.filter(user=self.request.user)  # replace to get_object.. or 404
#         if usertype == 'd':
#             return Doctor.objects.filter(user=self.request.user)
#         if usertype == 'c':
#             return get_object_or_404(Director, user=self.request.user)

# class ObjectMixin:

#     def get_object(self):
#         usertype=self.request.user.usertype
#         if usertype == 'p':
#             return get_object_or_404(Patient, user=self.request.user)
#         if usertype == 'd':
#             return get_object_or_404(Doctor, user=self.request.user)
#         if usertype == 'c':
#             return get_object_or_404(Director, user=self.request.user)

# class SerializerMixin:

#     def get_serializer_class(self):
#         usertype=self.request.user.usertype
#         if usertype == 'p':
#             return PatientUpdateSerializer
#         if usertype == 'd':
#             return DoctorUpdateSerializer
#         if usertype == 'c':
#             return DirectorUpdateSerializer


class UserAuthView(GenericViewSet):
    """
    View for User Login, Logout
    """
    permission_classes = [AllowAny]
    serializer_class=user_serializers.LoginUserSerializer

    @action(detail=False, methods=["post"], url_path='login')   # , serializer_class=LoginUserSerializer) 
    def user_login(self, request):                              # , *args, **kwargs):
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
    
    permission_classes = [AllowAny]

    def get_queryset(self):

        return User.objects.none()
       
    def get_serializer_class(self):
        if self.request.method == "POST":
            return user_serializers.UserRegisterSerializer
        if self.request.method == "GET":
            return user_serializers.UserRegisterSerializer


class UserUpdateView(RetrieveUpdateAPIView):
    """
    View for update User model
    """
# class UserUpdateView(UpdateAPIView):

    permission_classes=[IsAuthenticated]
    
    def get_queryset(self):

        return User.objects.all()
        

    def get_serializer_class(self):
        return user_serializers.UserUpdateSerializer

    def path(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

        
# class UserUpdateAPIView(generics.RetrieveUpdateAPIView):
#     permission_classes = (permissions.IsAdminUser,)
#     serializer_class = UserUpdateSerialier
#     lookup_field = 'username'

#     def get_object(self):
#         username = self.kwargs["username"]
#         return get_object_or_404(User, username=username)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
    
# 
class UserTypeCreateView(QuerysetMixin, SerializerMixin, ListCreateAPIView):
    """
    View for create Patient/Doctor/Director model
    """
 
    
    permission_classes = [IsAuthenticated, IsNotUserUpdated]

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except:
            raise ValidationError({"detail": "Operation not allowed"})
            
    
class UserTypeUpdateView(SerializerMixin, ObjectMixin, RetrieveUpdateAPIView): 
    """
    View for Update Patient/Doctor/Director model
    """

    permission_classes = [IsAuthenticated, IsUserUpdated]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

class UserPernamentDeleteView(SerializerMixin, ObjectMixin, RetrieveDestroyAPIView): 

    permission_classes = [IsAuthenticated]
    
    def destroy(self, request, *args, **kwargs):
        try:
            user = request.user
            user.delete()
            logout(request)
            return Response({"detail": "User deleted pernamently"})
        except:
            return Response({"detail": "User Cannot be deleted"})


class UserDeleteView(SerializerMixin, ObjectMixin, RetrieveDestroyAPIView): 
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


class UserListView(ReadOnlyModelViewSet):

    """
    User model List View (filtered list view)
    """

    # queryset=User.objects.all()
    permission_classes=[IsAuthenticated]
    # serializer_class=user_serializers.UserPublicSerializer


    def get_queryset(self):

        usertype=self.request.user.usertype
        if usertype == 'p':
            return User.objects.filter(id=self.request.user.id)
        
        if usertype == 'd':
            return User.objects.filter(id=self.request.user.id)

        if usertype == 'c':
            return User.objects.all()

    def get_serializer_class(self):

        usertype=self.request.user.usertype
        if usertype == 'p':
            return user_serializers.UserPublicSerializer

        
        if usertype == 'd':
            return user_serializers.UserPublicSerializer


        if usertype == 'c':
            return user_serializers.UserPublicSerializer


      