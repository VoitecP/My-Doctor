# from django.contrib.auth import logout as django_logout
from rest_framework.generics import  ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.core.models import *
from ..permissions import *
from ..serializers import doctor_serializers
from ..serializers.doctor_serializers import DoctorDynamicSerializer
from .view_mixins import ContextModelViewSet

from .view_mixins import ContextMixin, ContextModelViewSet
from .view_mixins import (ContextListCreateAPIView, 
                          ContextAPIView, ContextModelViewSet)  


class DoctorMixin:

    permission_classes = [IsAuthenticated, DoctorPermissions]
    serializer_class = DoctorDynamicSerializer

    def get_queryset(self):
        user = self.request.user
        if user.usertype == 'p':        
            return Doctor.objects.all()
        if user.usertype == 'd':
            return Doctor.objects.filter(user=user)
        if user.usertype == 'c' or user.is_staff:
            return Doctor.objects.all()
        return Doctor.objects.none()


class DoctorViewSet(DoctorMixin, ContextModelViewSet):
    
    pass
    
            
class DoctorListCreateView(DoctorMixin, ContextListCreateAPIView):
    """
    """
    pass


class DoctorAPIView(DoctorMixin, ContextAPIView):
    """
    """
    pass
  

        

    