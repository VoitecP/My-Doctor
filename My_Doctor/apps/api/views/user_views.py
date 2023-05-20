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

from rest_framework.generics import RetrieveUpdateAPIView, RetrieveDestroyAPIView, ListCreateAPIView
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
    

class UserRegisterView(ListCreateAPIView):
    
    permission_classes = [AllowAny]

    def get_queryset(self):
        return User.objects.none()
       
    def get_serializer_class(self):
        if self.request.method == "POST":
            return user_serializers.UserRegisterSerializer
        if self.request.method == "GET":
            return user_serializers.UserRegisterSerializer


class UserTypeUpdateView(QuerysetMixin, SerializerMixin, ListCreateAPIView):
    
    permission_classes = [IsAuthenticated, IsNotUserUpdated]

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except:
            raise ValidationError({"detail": "Operation not allowed"})
            
    
class UserProfileUpdateView(SerializerMixin, ObjectMixin, RetrieveUpdateAPIView): 

    permission_classes = [IsAuthenticated]

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




# for director only
class UserListView(ReadOnlyModelViewSet):

    queryset=User.objects.all()
    permission_classes=[IsAuthenticated,IsDoctor]
    serializer_class=user_serializers.UserPublicSerializer