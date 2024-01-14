from django.db.models import Sum
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from rest_framework.views import APIView
from rest_framework.response import Response  
from rest_framework.permissions import IsAuthenticated

from apps.api.serializers import summary_serializers
from apps.core.models import Visit
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
    """
    Return a summary view
    """
    permission_classes = [IsAuthenticated] #  , IsDoctorCreated]

    try:
        summary = Visit.objects.aggregate(sum=Sum('price'))
        total = Visit.objects.count()
    except:
        summary = None
        total = None
    
    def get(self, request, format=None):

        return Response({
            'Total Visits':self.total,
            'Total Sum':self.summary['sum']
            })







