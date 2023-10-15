from apps.core.models import Visit, Patient, Doctor, Director
from ..serializers import visit_serializers
from ..permissions import *
from ..permissions import IsDoctorCreated, IsPatientCreated, IsNotUserUpdated
from .view_mixins import UserQuerysetMixin, UserObjectMixin, UserSerializerMixin

from django.contrib.auth import login, logout, authenticate
from django.shortcuts import get_object_or_404

from rest_framework.response import Response  
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveDestroyAPIView,UpdateAPIView, CreateAPIView, ListCreateAPIView
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, GenericViewSet,  ReadOnlyModelViewSet
from rest_framework.serializers import ValidationError






class VisitListView(ReadOnlyModelViewSet):
    """
    Visit model List View (filtered list view)
    """
    # permission_classes=[IsAuthenticated, IsAdminUser, IsDirector]
    
    def get_queryset(self):
        usertype=self.request.user.usertype
        is_superuser=self.request.user.is_superuser
        id=self.request.user.id

        if is_superuser == True:
            return Visit.objects.all()     
        else:
            if usertype == 'p':
                return Visit.objects.filter(patient__pk=id)   
            if usertype == 'd':
                return Visit.objects.filter(doctor__pk=id)
            if usertype == 'c':
                return Visit.objects.all()
            

    def get_serializer_class(self):
        usertype=self.request.user.usertype

        if usertype == 'p':
            return visit_serializers.VisitPublicSerializer   
        if usertype == 'd':
            return visit_serializers.VisitPublicSerializer
        if usertype == 'c':
            return visit_serializers.VisitPublicSerializer
        


      

