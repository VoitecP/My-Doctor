from apps.core.models import *
from ..serializers import doctor_serializers
from ..permissions import *
from rest_framework import status
from rest_framework.viewsets import ModelViewSet


from rest_framework.response import Response  


# from django.contrib.auth import logout as django_logout
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.authentication import SessionAuthentication



class DoctorViewSet(ModelViewSet):
    # queryset=Doctor.objects.all()
    # serializer_class=doctor_serializers.DoctorPublicSerializer
    serializer_class=doctor_serializers.DoctorDynamicSerializer
    permission_classes = [IsAuthenticated]
    # http_method_names = ['get','post','retrieve','put','patch']
    

    def get_queryset(self):
        usertype=self.request.user.usertype
        if usertype == 'p':         # filter by visit
            return Doctor.objects.all()
        
        if usertype == 'd':
            # return Doctor.objects.filter(user=self.request.user)
            return Doctor.objects.all()

        if usertype == 'c':
            return Doctor.objects.all()
        
        

    def get_serializer_context(self):
        try:
            instance = self.get_object()
        except AssertionError:
            instance = None
   
        context = super().get_serializer_context()
        context.update({
            'request': self.request,   # exist in default
            'action': self.action,
            'instance': instance,
        })
        return context