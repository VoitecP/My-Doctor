from apps.core.models import Category
from rest_framework import serializers
# from apps.api.serializers import UserPublicSerializer


class CategoryPublicSerializer(serializers.ModelSerializer):
    """
    Public category serializer for all users
    """
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Category
        fields = '__all__'


class CategoryCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating Category
    """
    class Meta:
        model = Category
        fields = '__all__'
        

    def perform_create(self, validated_data):
        category = Category.objects.create(
            validated_data['name'], 
            validated_data['description'])
        category.name = validated_data['name']
        category.description = validated_data['description']
        # category.is_valid() # checks
        category.save()
        return category
    


    # def create(self, validated_data):
    #     user = User.objects.create_user(**validated_data)
    #     return user