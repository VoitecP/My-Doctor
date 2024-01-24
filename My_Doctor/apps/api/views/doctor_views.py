from rest_framework.permissions import IsAuthenticated

from ..permissions import DoctorPermissions
from ..serializers import DoctorDynamicSerializer
from ..views.view_mixins  import (ContextAPIView, ContextListCreateAPIView, 
                     ContextModelViewSet)  
from apps.core.models import Doctor


class DoctorMixin:

    permission_classes = [IsAuthenticated, DoctorPermissions]
    serializer_class = DoctorDynamicSerializer

    def get_queryset(self):
        user = self.request.user
        if user.usertype == 'p':        
            return Doctor.objects.all()
        if user.usertype == 'd':
            return Doctor.objects.filter(user=user)
        if user.usertype == 'c' or user.is_staff:
            return Doctor.objects.all()
        return Doctor.objects.none()


class DoctorViewSet(DoctorMixin, ContextModelViewSet):
    
    pass
    
            
class DoctorListCreateView(DoctorMixin, ContextListCreateAPIView):
    """
    """
    pass


class DoctorAPIView(DoctorMixin, ContextAPIView):
    """
    """
    pass
  

        

    