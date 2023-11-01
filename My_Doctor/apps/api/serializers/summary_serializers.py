from apps.core.models import Visit
from rest_framework import serializers

from ..serializers import visit_serializers
from .doctor_serializers import DoctorPublicSerializer, DoctorPrivateSerializer, DoctorVisitSerializer
from .patient_serializers import PatientPublicSerializer, PatientPrivateSerializer, PatientVisitSerializer

# from apps.api.serializers import UserPublicSerializer, UserUpdateSerializer, UserPrivateSerializer  

# class UserSerializer(serializers.ModelSerializer):
#     days_since_joined = serializers.SerializerMethodField()

#     class Meta:
#         model = User
#         fields = '__all__'

#     def get_days_since_joined(self, obj):
#         return (now() - obj.date_joined).days





class VisitYearSummarySerializer(serializers.ModelSerializer):
    """
    Serializer Summary View
    """
    year=serializers.IntegerField(source='date__year')
    total=serializers.IntegerField()
    sum=serializers.IntegerField()

    class Meta:
        model = Visit
        fields =['year','total','sum']
    

class VisitMonthSummarySerializer(serializers.ModelSerializer):
    """
    Serializer Summary View
    """
    month=serializers.IntegerField(source='date__month')
    year=serializers.IntegerField(source='date__year')
    total=serializers.IntegerField()
    sum=serializers.IntegerField()

    class Meta:
        model = Visit
        fields =['month','year','total','sum']

# class VisitSummary2Serializer(serializers.ModelSerializer):
#     
#   
#     sum=serializers.IntegerField()
#     year=serializers.IntegerField(source='date__year')

#     class Meta:
#         model = Visit
#         # fields = '__all__'      # only price, patient and doctor fields
#         # fields =['id','tracks','patient','doctor','price']
#         fields =['id','tracks','patient','doctor','year','sum']






