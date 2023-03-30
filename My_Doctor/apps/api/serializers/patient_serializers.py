from apps.core.models import Patient
from rest_framework import serializers

class PatientSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Patient
        fields = '__all__'