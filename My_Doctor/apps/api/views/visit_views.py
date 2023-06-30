from apps.core.models import Visit, Patient, Doctor, Director
from ..serializers import visit_serializers
# from ..serializers.patient_serializers import PatientUpdateSerializer
# from ..serializers.doctor_serializers import DoctorUpdateSerializer
# from ..serializers.director_serializers import DirectorUpdateSerializer
from ..permissions import *
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, GenericViewSet,  ReadOnlyModelViewSet
from rest_framework.serializers import ValidationError

from django.contrib.auth import login, logout, authenticate
from rest_framework.response import Response  
from rest_framework.decorators import action

# from django.contrib.auth import logout as django_logout
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.generics import RetrieveUpdateAPIView, RetrieveDestroyAPIView,UpdateAPIView, CreateAPIView, ListCreateAPIView
from ..permissions import IsDoctorCreated, IsPatientCreated, IsNotUserUpdated

from django.shortcuts import get_object_or_404

from .mixins import QuerysetMixin, ObjectMixin, SerializerMixin



class VisitListView(ReadOnlyModelViewSet):

    """
    Visit model List View (filtered list view)
    """

    # queryset=User.objects.all()
    permission_classes=[IsAuthenticated]
    # serializer_class=user_serializers.UserPublicSerializer


    def get_queryset(self):

        usertype=self.request.user.usertype
        if usertype == 'p':
            return Visit.objects.filter(patient__pk=self.request.user.id)
        
        if usertype == 'd':
            return Visit.objects.filter(doctor__pk=self.request.user.id)

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


      

