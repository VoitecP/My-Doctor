from apps.core.models import *
from ..serializers import *
from ..permissions import *
from rest_framework import status
from rest_framework.viewsets import  ModelViewSet


from rest_framework.response import Response  
from rest_framework.decorators import action

# from django.contrib.auth import logout as django_logout
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.authentication import SessionAuthentication
from ..permissions import IsDoctorCreated, IsPatientCreated



class PatientViewset(ModelViewSet):
    # queryset=Patient.objects.all()
    # serializer_class=PatientPrivateSerializer
    # TODO usertype serializers
    #serializer_class=PatientForDoctorSerializer
    permission_classes = [IsAuthenticated] #  , IsDoctorCreated]       No other perm_class
    # http_method_names = ['get']
    

    def get_queryset(self):
        usertype=self.request.user.usertype
        if usertype == 'd':      
            return Patient.objects.filter(visit__doctor__user=self.request.user).distinct()
            # Patient Visit serializer add visit count.. with that doctor     
        if usertype == 'p':        
            return Patient.objects.filter(user=self.request.user)
            # Patient Private Serializer
        if usertype == 'c':
            return Patient.objects.all()

    def get_serializer_class(self):
        usertype=self.request.user.usertype
        if usertype == 'd':  
            return PatientForDoctorSerializer
        if usertype == 'p':  
            return PatientForPatientSerializer
        if usertype == 'c':  
            return PatientForDoctorSerializer
        