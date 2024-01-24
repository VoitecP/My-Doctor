from rest_framework.permissions import IsAuthenticated

from ..permissions import DirectorPermissions
from ..serializers import(DirectorDynamicSerializerForDirector, 
                          DirectorDynamicSerializerForPerson)
from ..views.view_mixins  import (ContextAPIView, ContextListCreateAPIView, 
                     ContextModelViewSet)  
from apps.core.models import  Director


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
            return DirectorDynamicSerializerForDirector
        return DirectorDynamicSerializerForPerson


class DirectorViewSet(DirectorMixin, ContextModelViewSet):
    '''
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
  

