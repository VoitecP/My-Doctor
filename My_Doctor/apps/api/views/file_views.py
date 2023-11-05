from apps.core.models import *
from ..serializers import file_serializers
from ..permissions import *
from rest_framework import status
from rest_framework.viewsets import ReadOnlyModelViewSet


from rest_framework.response import Response  


# from django.contrib.auth import logout as django_logout
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.authentication import SessionAuthentication

from rest_framework.generics import RetrieveUpdateAPIView, RetrieveDestroyAPIView, ListCreateAPIView, DestroyAPIView
from rest_framework.serializers import ValidationError




class PatientPhotoListView(ReadOnlyModelViewSet):
   
    serializer_class=file_serializers.PatientPhotoSerializer
    permission_classes = [IsAuthenticated]
    # http_method_names = ['get','post','retrieve','put','patch']
    
    def get_queryset(self):
        return PatientPhotoFile.objects.filter(user=self.request.user)
       


class PatientPhotoCreateView(ListCreateAPIView):
    """
    View for create PatientPhoto model
    """
    #permission_classes = [IsAdminUser, IsDirector] 


    def get_queryset(self):
        return PatientPhotoFile.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        return file_serializers.PatientPhotoCreateSerializer
    
    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
            return Response({"detail": "Success"})
        except:
            raise ValidationError({"detail": "Operation not allowed"})