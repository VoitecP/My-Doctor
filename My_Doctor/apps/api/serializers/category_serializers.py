from apps.core.models import Category
from rest_framework import serializers
# from apps.api.serializers import UserPublicSerializer


class CategoryPublicSerializer(serializers.ModelSerializer):
    """
    Public category serializer for all users
    """
    
    class Meta:
        model = Category
        fields = ['name','description']
        extra_kwargs = {'name': {'read_only': True},
                        'description': {'read_only': True}
                        }


class CategoryCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating Category
    """
    class Meta:
        model = Category
        fields = ['name','description']
        

    def perform_create(self, validated_data):
        category = Category.objects.create(
            validated_data['name'], 
            validated_data['description'])
        category.name = validated_data['name']
        category.description = validated_data['description']
        # category.is_valid() # checks
        category.save()
        return category
    