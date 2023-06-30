from apps.core.models import Visit
from rest_framework import serializers
from .doctor_serializers import DoctorPublicSerializer, DoctorPrivatecSerializer, DoctoVisitSerializer
from .patient_serializers import PatientPublicSerializer, PatientPrivateSerializer, PatientVisitSerializer


class VisitPublicSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    doctor = DoctorPublicSerializer(read_only=True)
    patient = PatientPublicSerializer(read_only=True)

    class Meta:
        model = Visit
        fields = '__all__'


class VisitPrivateSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    doctor = DoctorPublicSerializer(read_only=True)
    patient = PatientPublicSerializer(read_only=True)

    class Meta:
        model = Visit
        fields = '__all__'


class VisitVisitSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    doctor = DoctorPublicSerializer(read_only=True)
    patient = PatientPublicSerializer(read_only=True)

    class Meta:
        model = Visit
        fields = '__all__'


###


# class LoginUserSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(write_only=True, required=True)
#     password = serializers.CharField(write_only=True, required=True)
    
#     class Meta:
#         model = User
#         fields = ['username', 'password']


# class DoctorPublicSerializer(serializers.ModelSerializer):
#     tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
#     user = UserPublicSerializer(read_only=True)
    
#     class Meta:
#         model = Doctor
#         fields = ['tracks','user','specialization','phone']
#         # fields = '__all__'