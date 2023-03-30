from apps.core.models import *
from ..serializers import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

class PatientViewSet(ModelViewSet):
    queryset=Patient.objects.all()
    #serializer_class=PatientSerializer
    permission_classes=[IsAuthenticated]
    
    
    # filter_backends=[DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_class=PatientFilter        
    # search_fields=['name','surname','citizen_id']
    # ordering_fields=['citizen_id', 'name', 'surname'] 
