from apps.core.models import User, Patient, Doctor, Director
from ..serializers import user_serializers
from ..serializers.patient_serializers import PatientUpdateSerializer
from ..serializers.doctor_serializers import DoctorUpdateSerializer
from ..serializers.director_serializers import DirectorUpdateSerializer
from ..permissions import *
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, GenericViewSet,  ReadOnlyModelViewSet
from rest_framework.serializers import ValidationError

from django.contrib.auth import login, logout, authenticate
from rest_framework.response import Response  
from rest_framework.decorators import action

# from django.contrib.auth import logout as django_logout
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.generics import RetrieveUpdateAPIView, RetrieveDestroyAPIView, ListCreateAPIView
from ..permissions import IsDoctorCreated, IsPatientCreated, IsNotUserUpdated

from django.shortcuts import get_object_or_404
from .mixins import QuerysetMixin, ObjectMixin, SerializerMixin



class UserProfileUpdateView(SerializerMixin, ObjectMixin, RetrieveUpdateAPIView): 

    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)