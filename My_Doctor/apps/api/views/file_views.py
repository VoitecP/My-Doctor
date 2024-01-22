# from django.contrib.auth import logout as django_logout
from rest_framework import status
from rest_framework.generics import (
    RetrieveUpdateAPIView, RetrieveDestroyAPIView, 
    ListCreateAPIView, DestroyAPIView)
from rest_framework.generics import  ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response  
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.serializers import ValidationError
from rest_framework.viewsets import ModelViewSet

from ..serializers.file_serializers import VisitImageDynamicSerializer
from ..serializers import file_serializers 
from ..permissions import FilePermissions
from .view_mixins import (ContextListCreateAPIView, 
                          ContextAPIView, ContextModelViewSet) 
from apps.core.models import *


class VisitImageMixin:

    permission_classes = [IsAuthenticated, FilePermissions] 
    serializer_class = VisitImageDynamicSerializer

    def get_queryset(self):
        user = self.request.user
        if user.usertype == 'p':
            return VisitImageFile.objects.filter(visit__patient__pk=user.id)    
        elif user.usertype == 'd':
            return VisitImageFile.objects.filter(visit__doctor__pk=user.id)  
        elif (user.usertype == 'c' or user.is_staff):
            return VisitImageFile.objects.all()
        return Visit.objects.none()


class VisitImageViewSet(VisitImageMixin, ContextModelViewSet):
    
    pass
       

class VisitImageListCreateView(VisitImageMixin,  ContextListCreateAPIView):
    """
    """
    pass


class VisitImageAPIView(VisitImageMixin, ContextAPIView):
    """
    """
    pass


# Todo Multiple image not working properly with VisitImage model 

class PatientImageViewSet(ModelViewSet):
   
    serializer_class=file_serializers.PatientImageSerializer
    permission_classes = [IsAuthenticated]
    # http_method_names = ['get','post','retrieve','put','patch']
    
    def get_queryset(self):
        return VisitImageFile.objects.filter(user=self.request.user)
       


class PatientImageCreateView(ListCreateAPIView):
    """
    View for create PatientImage model
    """
    #permission_classes = [IsAdminUser, IsDirector] 


    def get_queryset(self):
        return VisitImageFile.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        return file_serializers.PatientImageCreateSerializer
    
    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
            return Response({"detail": "Success"})
        except:
            raise ValidationError({"detail": "Operation not allowed"})
        




class PatientImageDeleteView(RetrieveDestroyAPIView):
    """
    View for Delete Image model
    """
    #permission_classes=[IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        return VisitImageFile.objects.none()
   
    def get_serializer_class(self):
        return file_serializers.PatientImageDeleteSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            Image = self.get_object()
            self.perform_destroy(Image)
            return Response({"detail": "Image deleted"})
        except:
           return Response({"detail": "Image Cannot be deleted"})