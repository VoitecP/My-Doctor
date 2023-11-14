from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from rest_framework.views import APIView
from apps.api.serializers import summary_serializers
from apps.core.models import Visit
from rest_framework.response import Response  

from django.db.models import Sum
from rest_framework.permissions import IsAuthenticated
# from ..permissions import IsDoctorCreated

class SummaryYearVisitListView(ReadOnlyModelViewSet):
    queryset=Visit.year_objects.all()
    serializer_class=summary_serializers.VisitYearSummarySerializer
    #permission_classes = [IsAuthenticated] #  , IsDoctorCreated]       No other perm_class
    # http_method_names = ['get']


class SummaryMonthVisitListView(ReadOnlyModelViewSet):
    queryset=Visit.month_objects.all()
    serializer_class=summary_serializers.VisitMonthSummarySerializer


class SummaryCategoryVisitListView(ReadOnlyModelViewSet):
    queryset=Visit.category_objects.all()
    serializer_class=summary_serializers.VisitCategorySummarySerializer


class SummaryDoctorVisitListView(ReadOnlyModelViewSet):
    queryset=Visit.doctor_objects.all()
    serializer_class=summary_serializers.VisitDoctorSummarySerializer


class SummaryVisitView(APIView):
#class SummaryVisitView(GenericViewSet):
    """
    Return a summary view
    """
    permission_classes = [IsAuthenticated] #  , IsDoctorCreated]

    summary=Visit.objects.aggregate(sum=Sum('price'))
    total=Visit.objects.count()
    
    def get(self, request, format=None):
        return Response({'Price Summary':self.summary['sum'],
                         'Total Visits':self.total
                         })







