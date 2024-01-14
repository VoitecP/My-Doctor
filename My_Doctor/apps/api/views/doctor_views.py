from apps.core.models import *
from ..serializers import doctor_serializers
from ..permissions import *
from rest_framework import status
from rest_framework.viewsets import ModelViewSet


from rest_framework.response import Response  


# from django.contrib.auth import logout as django_logout
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.authentication import SessionAuthentication
from .view_mixins import ContextModelViewSet


class DoctorViewSet(ContextModelViewSet):
    
    serializer_class=doctor_serializers.DoctorDynamicSerializer
    permission_classes = [IsAuthenticated, DoctorPermissions]
    # http_method_names = ['get','post','retrieve','put','patch']
    

    def get_queryset(self):
        user = self.request.user

        if user.usertype == 'p':         # filter by visit
            return Doctor.objects.all()
        if user.usertype == 'd':
            return Doctor.objects.filter(user=user)
            #return Doctor.objects.all()
        if user.usertype == 'c':
            return Doctor.objects.all()
        

    