from apps.core.models import Patient, User, Doctor
from ..serializers import user_serializers
from ..serializers.patient_serializers import PatientUpdateSerializer
from ..serializers.doctor_serializers import DoctorUpdateSerializer
from ..permissions import *
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, GenericViewSet,  ReadOnlyModelViewSet
from rest_framework.serializers import ValidationError

from django.contrib.auth import login, logout, authenticate
from rest_framework.response import Response  
from rest_framework.decorators import action

# from django.contrib.auth import logout as django_logout
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.generics import ListCreateAPIView
from ..permissions import IsDoctorCreated, IsPatientCreated, IsNotUserUpdated



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
        # user=self.request.user
        # return Patient.objects.filter(user=user)
        return User.objects.none()
       

    def get_serializer_class(self):

        if self.request.method == "POST":
            return user_serializers.UserRegisterSerializer
        
        if self.request.method == "GET":
            return user_serializers.UserRegisterSerializer




## User register serializer  + Patient serializer

class UserTypeUpdateView(ListCreateAPIView):

    permission_classes = [IsAuthenticated, IsNotUserUpdated]

    def get_queryset(self):
        usertype=self.request.user.usertype
        if usertype == 'p':
            return Patient.objects.filter(user=self.request.user)
        if usertype == 'd':
            return Doctor.objects.filter(user=self.request.user)
            

    def get_serializer_class(self):

        usertype=self.request.user.usertype
        if usertype == 'p':
            return PatientUpdateSerializer
        if usertype == 'd':
            return DoctorUpdateSerializer

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except:
            raise ValidationError({"detail": "Operation not allowed"})
            
    

# for director only
class UserListView(ReadOnlyModelViewSet):

    queryset=User.objects.all()
    permission_classes=[IsAuthenticated,IsDoctor]
    serializer_class=user_serializers.UserPublicSerializer