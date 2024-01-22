from rest_framework.generics import  ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.serializers import ValidationError
from rest_framework.response import Response  
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.core.models import  Director
from ..permissions import *
# from apps.core.permissions import IsDoctorCreated, IsPatientCreated, IsNotUserUpdated
from ..serializers import director_serializers
from ..serializers.director_serializers import(
            DirectorDynamicSerializerForDirector, DirectorDynamicSerializerForPerson)
from .view_mixins import ContextMixin, ContextModelViewSet 
from .view_mixins import (ContextListCreateAPIView, 
                          ContextAPIView, ContextModelViewSet)  



class DirectorMixin:

    permission_classes = [IsAuthenticated, DirectorPermissions]

    def get_queryset(self):
        user = self.request.user
        if user.usertype == 'p':        
            return Director.objects.all()
        if user.usertype == 'd':
            return Director.objects.filter(user=user)
        if user.usertype == 'c' or user.is_staff:
            return Director.objects.all()
        return Director.objects.none()


    def get_serializer_class(self):
        user=self.request.user
        if user.usertype == 'c' or user.is_staff:
            return director_serializers.DirectorDynamicSerializerForDirector
        return director_serializers.DirectorDynamicSerializerForPerson


class DirectorViewSet(DirectorMixin, ContextModelViewSet):
    '''
    Viewset for Director model. Required dynamic serializers 
    and specyfic permission class for managing action access
    '''
    pass


class DirectorListCreateView(DirectorMixin, ContextListCreateAPIView):
    """
    """
    pass


class DirectorAPIView(DirectorMixin, ContextAPIView):
    """
    """
    pass
  

    

#####
# ApiViews
#####
class DirectorCreateView(ListCreateAPIView):
    queryset=Director.objects.all()
    #serializer_class=director_serializers.DirectorCreateSerializer
    # permission_classes = [IsAuthenticated,DirectorSingletonPermission]

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