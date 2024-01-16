# from django.contrib.auth import logout as django_logout
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.core.models import *
from ..permissions import *
from ..serializers import doctor_serializers
from .view_mixins import ContextModelViewSet


class DoctorViewSet(ContextModelViewSet):
    
    serializer_class=doctor_serializers.DoctorDynamicSerializer
    permission_classes = [IsAuthenticated, DoctorPermissions]
    # permission_classes = [DoctorPermissions]
    # http_method_names = ['get','post','retrieve','put','patch']
    

    def get_queryset(self):
        user = self.request.user

        if user.usertype == 'p':         # filter by visit
            return Doctor.objects.all()
        if user.usertype == 'd':
            return Doctor.objects.filter(user=user)
            #return Doctor.objects.all()
        if user.usertype == 'c' or user.is_staff:
            return Doctor.objects.all()
        
        

    