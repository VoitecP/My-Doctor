from apps.core.models import Visit
from rest_framework import serializers
from django.db.models import Sum, Aggregate

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
    Serializer For Visit Category Summary View
    """
    category=serializers.CharField(source='category_name')
    total=serializers.IntegerField()
    sum=serializers.IntegerField()

    class Meta:
        model = Visit
        fields =['category','total','sum']


class VisitDoctorSummarySerializer(serializers.ModelSerializer):
    """
    Serializer For Visit Doctor Summary View
    """
    id=serializers.UUIDField(source='doctor_id')
    name=serializers.CharField(source='doctor__user__first_name')
    surname=serializers.CharField(source='doctor__user__last_name')
    total=serializers.IntegerField()
    sum=serializers.IntegerField()

    class Meta:
        model = Visit
        fields =['id','name','surname','total','sum']
        # fields =['id','sum']

