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

#####
# Viewsets
#####

class DirectorViewset(ModelViewSet):
    '''
    Viewset for Director model. Required dynamic serializers 
    and specyfic permission class for managing action access
    '''
    permission_classes = [IsAuthenticated, DirectorPermissions]
    queryset = Director.objects.all()
    

    def get_serializer_class(self):
        usertype=self.request.user.usertype
        is_staff=self.request.user.is_staff

        if usertype == 'p' or usertype == 'd':
            return director_serializers.DirectorDynamicSerializerForPerson
        
        if usertype == 'c' or is_staff == True:
            return director_serializers.DirectorDynamicSerializerForDirector
            
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'request': self.request,   # exist in default
            'action': self.action,
        })
        return context
    



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