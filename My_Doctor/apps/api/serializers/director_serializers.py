from apps.core.models import Doctor
from rest_framework import serializers
from apps.api.serializers import UserPublicSerializer

class DirectorUpdateSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Doctor
        fields = '__all__'
