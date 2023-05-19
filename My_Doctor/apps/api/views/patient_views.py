from apps.core.models import *
from ..serializers import *
from ..permissions import *
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, GenericViewSet, ReadOnlyModelViewSet

from django.contrib.auth import login, logout, authenticate
from rest_framework.response import Response  
from rest_framework.decorators import action

# from django.contrib.auth import logout as django_logout
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.authentication import SessionAuthentication
from ..permissions import IsDoctorCreated, IsPatientCreated



class PatientListView(ReadOnlyModelViewSet):
    # queryset=Patient.objects.all()
    serializer_class=PatientPublicSerializer
    permission_classes = [IsAuthenticated, IsDoctorCreated]
    # http_method_names = ['get']
    

    def get_queryset(self):
        usertype=self.request.user.usertype
        if usertype == 'd':
            return Patient.objects.all()
        
        if usertype == 'p':
            return Patient.objects.filter(user=self.request.user)
