from apps.core.models import Visit
from rest_framework import serializers

from ..serializers import visit_serializers
from .doctor_serializers import DoctorPublicSerializer, DoctorPrivateSerializer, DoctorVisitSerializer
from .patient_serializers import PatientPublicSerializer, PatientPrivateSerializer, PatientVisitSerializer


class VisitYearSummarySerializer(serializers.ModelSerializer):
    """
    Serializer For Visit Year Summary View
    """
    year=serializers.IntegerField(source='date__year')
    total=serializers.IntegerField()
    sum=serializers.IntegerField()

    class Meta:
        model = Visit
        fields =['year','total','sum']
    

class VisitMonthSummarySerializer(serializers.ModelSerializer):
    """
    Serializer For Visit Month/Year Summary View
    """
    month=serializers.IntegerField(source='date__month')
    year=serializers.IntegerField(source='date__year')
    total=serializers.IntegerField()
    sum=serializers.IntegerField()

    class Meta:
        model = Visit
        fields =['month','year','total','sum']


class VisitCategorySummarySerializer(serializers.ModelSerializer):
    """
    Serializer For Visit Month/Year Summary View
    """
    category=serializers.CharField(source='category_name')
    total=serializers.IntegerField()
    sum=serializers.IntegerField()

    class Meta:
        model = Visit
        fields =['category','total','sum']





