from rest_framework.generics import (
    RetrieveUpdateAPIView, RetrieveDestroyAPIView, 
    ListCreateAPIView)
from rest_framework.serializers import ValidationError
from rest_framework.response import Response  
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.core.models import  Director
from ..permissions import *
from ..permissions import IsDoctorCreated, IsPatientCreated, IsNotUserUpdated
from ..serializers import director_serializers
from .view_mixins import ContextModelViewSet


#####
# Viewsets

class DirectorViewSet(ContextModelViewSet):
    '''
    Viewset for Director model. Required dynamic serializers 
    and specyfic permission class for managing action access
    '''
    permission_classes = [IsAuthenticated, DirectorPermissions]
    queryset = Director.objects.all()
    
    def get_serializer_class(self):
        user=self.request.user
    
        if user.usertype in ['p','d']:
            return director_serializers.DirectorDynamicSerializerForPerson
        
        if user.usertype == 'c' or user.is_staff:
            return director_serializers.DirectorDynamicSerializerForDirector
            

    

#####
# ApiViews
#####
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
        



    
# class DirectorUpdateView(RetrieveUpdateAPIView):
#     queryset=Director.objects.all()
#     serializer_class=director_serializers.DirectorUpdateSerializer


# class DirectorDeleteView(RetrieveDestroyAPIView):
#     queryset=Director.objects.all()
#     serializer_class=director_serializers.DirectorDeleteSerializer





# if usertype == 'p' or usertype == 'd':
#             if self.action in ['list', 'create']:
#                 return director_serializers.DirectorDynamicSerializerForPerson
#             if self.action in ['retrieve', 'destroy']:
#                 return director_serializers.DirectorDynamicSerializerForPerson
#             if self.action in ['update','partial_update']:
#                 return director_serializers.DirectorDynamicSerializerForPerson