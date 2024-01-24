from rest_framework.permissions import IsAuthenticated

from ..permissions import VisitPermissions
from ..serializers import VisitDynamicSerializer
from ..views.view_mixins  import (ContextListCreateAPIView, 
                                ContextAPIView, 
                                ContextModelViewSet) 
from apps.core.models import Visit


class VisitMixin:

    permission_classes=[IsAuthenticated, VisitPermissions]
    serializer_class = VisitDynamicSerializer

    def get_queryset(self):
        user=self.request.user
        if user.usertype == 'p':
            return Visit.objects.filter(patient__user=user)
        elif user.usertype == 'd':
            return Visit.objects.filter(doctor__user=user)
        elif (user.usertype == 'c' or user.is_staff):
            return Visit.objects.all()
        return Visit.objects.none()


class VisitViewSet(VisitMixin, ContextModelViewSet):
    """
    """
    pass
    

class VisitListCreateView(VisitMixin, ContextListCreateAPIView):
    """
    """
    pass

    
class VisitAPIView(VisitMixin, ContextAPIView):
    """
    """
    pass


   
