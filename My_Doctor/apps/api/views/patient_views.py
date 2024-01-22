# from django.contrib.auth import logout as django_logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response  
from rest_framework.viewsets import  ModelViewSet
from rest_framework.generics import  ListCreateAPIView, RetrieveUpdateDestroyAPIView

from ..permissions import *
from ..serializers import *
from ..serializers.patient_serializers import PatientDynamicSerializer
from .view_mixins import (ContextListCreateAPIView, 
                          ContextAPIView, ContextModelViewSet) 
from apps.core.models import *


class PatientMixin:

    permission_classes = [IsAuthenticated, PatientPermissions]
    serializer_class = PatientDynamicSerializer

    def get_queryset(self):
        user = self.request.user
        if user.usertype == 'p':         
            return Patient.objects.filter(user=user)
        elif user.usertype == 'd':
            return Patient.objects.filter(visit__doctor__user=user).distinct()
            #return Patient.objects.all()
        elif user.usertype == 'c' or user.is_staff:
            return Patient.objects.all()
        return Patient.objects.none()


class PatientViewSet(PatientMixin, ContextModelViewSet): 
    
    pass

    
class PatientListCreateView(PatientMixin, ContextListCreateAPIView):
    """
    """
    pass


class PatientAPIView(PatientMixin, ContextAPIView):
    """
    """
    pass


# Junk Viewset
class Patient2Viewset(ModelViewSet):
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
        