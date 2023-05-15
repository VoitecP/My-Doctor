from apps.core.models import *
from ..serializers import *
from ..permissions import *
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from django.contrib.auth import login, logout, authenticate
from rest_framework.response import Response  
from rest_framework.decorators import action

# from django.contrib.auth import logout as django_logout
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.authentication import SessionAuthentication




class PatientViewSet(ModelViewSet):
    # queryset=Patient.objects.all()
    serializer_class=PatientPublicSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get','post','retrieve','put','patch']
    

    def get_queryset(self):
        user=self.request.user
        if user.usertype == 'd':
            return Patient.objects.all()
        
        if user.usertype == 'p':
            return Patient.objects.filter(user=user)
