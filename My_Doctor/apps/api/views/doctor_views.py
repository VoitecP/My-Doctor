from apps.core.models import *
from ..serializers import doctor_serializers
from ..permissions import *
from rest_framework import status
from rest_framework.viewsets import ReadOnlyModelViewSet


from rest_framework.response import Response  


# from django.contrib.auth import logout as django_logout
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.authentication import SessionAuthentication



class DoctorListView(ReadOnlyModelViewSet):
    # queryset=Patient.objects.all()
    serializer_class=doctor_serializers.DoctorPublicSerializer
    permission_classes = [IsAuthenticated]
    # http_method_names = ['get','post','retrieve','put','patch']
    

    def get_queryset(self):
        usertype=self.request.user.usertype
        if usertype == 'p':         # filter by visit
            return Doctor.objects.all()
        
        if usertype == 'd':
            return Doctor.objects.filter(user=self.request.user)

        if usertype == 'c':
            return Doctor.objects.all()