from apps.core.models import Director
from rest_framework import serializers
from apps.api.serializers import UserPublicSerializer, user_serializers


class DirectorPublicSerializer(serializers.ModelSerializer):
    """
    All patient's and doctor's can see 
    """
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    user = user_serializers.UserPublicSerializer(read_only=True)
    
    class Meta:
        model = Director
        # fields = '__all__'
        fields = ['user','description','tracks']


class DirectorPrivateSerializer(serializers.ModelSerializer):
    """
    Only director can see self fields
    """
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    user = user_serializers.UserPrivateSerializer(read_only=True)

    class Meta:
        model = Director
        # fields = '__all__'
        fields = ['user','description','tracks']


###

class DirectorUpdateSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Director
        fields = '__all__'

