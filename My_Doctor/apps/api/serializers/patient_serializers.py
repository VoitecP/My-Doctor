from apps.core.models import Patient
from rest_framework import serializers

class PatientSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Patient
        fields = '__all__'


##

class PatientPrivateSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Patient
        fields = '__all__'


class PatientPublicSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Patient
        fields = ['first_name','last_name']


class PatientVisitSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Patient
        fields = '__all__'