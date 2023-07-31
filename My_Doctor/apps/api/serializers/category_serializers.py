from apps.core.models import Category
from rest_framework import serializers
# from apps.api.serializers import UserPublicSerializer


class CategoryPublicSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Category
        fields = '__all__'


class CategoryPrivateSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Category
        fields = '__all__'


###

