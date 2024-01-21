from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from ..permissions import VisitPermissions
from ..serializers import VisitDynamicSerializer
from .view_mixins import ContextModelViewSet, ContextMixin
from apps.core.models import Visit


class QuerysetMixin:

    def perform_queryset(self):
        user=self.request.user
        if user.usertype == 'p':
            return Visit.objects.filter(patient__user=user)
        elif user.usertype == 'd':
            return Visit.objects.filter(doctor__user=user)
        elif (user.usertype == 'c' or user.is_staff):
            return Visit.objects.all()
        return Visit.objects.none()



class VisitViewSet(QuerysetMixin, ContextModelViewSet):
    """
    """
    permission_classes=[IsAuthenticated, VisitPermissions]
    serializer_class = VisitDynamicSerializer

    def get_queryset(self):
        return self.perform_queryset()
    
    

class VisitListCreateView(ContextMixin, QuerysetMixin, 
                          ListCreateAPIView):
    """
    """
    permission_classes = [IsAuthenticated, VisitPermissions] 
    serializer_class = VisitDynamicSerializer

    def get_queryset(self):
        return self.perform_queryset()
    

    
class VisitAPIView(ContextMixin, QuerysetMixin, 
                   RetrieveUpdateDestroyAPIView):
    """
    """
    permission_classes = [IsAuthenticated, VisitPermissions]
    serializer_class = VisitDynamicSerializer

    def get_queryset(self):
        return self.perform_queryset()


