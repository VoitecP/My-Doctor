from apps.core.models import Director
from rest_framework import serializers
from apps.api.serializers import UserPublicSerializer

class DirectorUpdateSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Director
        fields = '__all__'



class DirectorPublicSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Director
        fields = '__all__'
