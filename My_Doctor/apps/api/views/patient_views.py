from rest_framework.permissions import IsAuthenticated

from ..permissions import PatientPermissions
from ..serializers import PatientDynamicSerializer
from ..views.view_mixins  import (ContextAPIView,
                     ContextListCreateAPIView,           
                     ContextModelViewSet) 
from apps.core.models import Patient


class PatientMixin:

    permission_classes = [IsAuthenticated, PatientPermissions]
    serializer_class = PatientDynamicSerializer

    def get_queryset(self):
        user = self.request.user
        if user.usertype == 'p':         
            return Patient.objects.filter(user=user)
        elif user.usertype == 'd':
            return Patient.objects.filter(visit__doctor__user=user).distinct()
            #return Patient.objects.all()
        elif user.usertype == 'c' or user.is_staff:
            return Patient.objects.all()
        return Patient.objects.none()


class PatientViewSet(PatientMixin, ContextModelViewSet): 
    
    pass

    
class PatientListCreateView(PatientMixin, ContextListCreateAPIView):
    """
    """
    pass


class PatientAPIView(PatientMixin, ContextAPIView):
    """
    """
    pass

