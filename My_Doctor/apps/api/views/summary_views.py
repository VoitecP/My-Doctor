from rest_framework.viewsets import ReadOnlyModelViewSet
from apps.api.serializers import summary_serializers
from apps.core.models import Visit


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