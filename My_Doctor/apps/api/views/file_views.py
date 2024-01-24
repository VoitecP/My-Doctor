from rest_framework.permissions import IsAuthenticated

from ..serializers import VisitImageDynamicSerializer 
from ..permissions import FilePermissions
from ..views.view_mixins  import (ContextAPIView,
                     ContextListCreateAPIView, 
                     ContextModelViewSet) 
from apps.core.models import VisitImageFile


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
        return VisitImageFile.objects.none()


class VisitImageViewSet(VisitImageMixin, ContextModelViewSet):
    '''
    '''
    pass
       

class VisitImageListCreateView(VisitImageMixin,  ContextListCreateAPIView):
    """
    """
    pass


class VisitImageAPIView(VisitImageMixin, ContextAPIView):
    """
    """
    pass



