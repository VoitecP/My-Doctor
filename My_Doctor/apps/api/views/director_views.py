from apps.core.models import  Director
from ..serializers import director_serializers
from ..permissions import *
from rest_framework import status
from rest_framework.viewsets import   ModelViewSet
from rest_framework.serializers import ValidationError


from rest_framework.response import Response  
from rest_framework.decorators import action

from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.generics import RetrieveUpdateAPIView, RetrieveDestroyAPIView, ListCreateAPIView
from ..permissions import IsDoctorCreated, IsPatientCreated, IsNotUserUpdated

from django.shortcuts import get_object_or_404
from .view_mixins import UserQuerysetMixin, UserObjectMixin, UserSerializerMixin

class DirectorViewset(ModelViewSet):
    queryset=Director.objects.all()
    serializer_class=director_serializers.DirectorPublicSerializer
    permission_classes = [IsAuthenticated]
    # http_method_names = ['get','post','retrieve','put','patch']


class DirectorCreateView(ListCreateAPIView):
    queryset=Director.objects.all()
    #serializer_class=director_serializers.DirectorCreateSerializer
    permission_classes = [IsAuthenticated,DirectorSingletonPermission]

    def get_serializer_class(self):
        return director_serializers.DirectorCreateSerializer
        
    def perform_create(self, serializer):
        try:
            serializer.save()
            return Response({"detail": "Success"})
        except:
            raise ValidationError({"detail": "Operation not allowed"})
        



    
class DirectorUpdateView(RetrieveUpdateAPIView):
    queryset=Director.objects.all()
    serializer_class=director_serializers.DirectorUpdateSerializer


class DirectorDeleteView(RetrieveDestroyAPIView):
    queryset=Director.objects.all()
    serializer_class=director_serializers.DirectorDeleteSerializer
