from apps.core.models import Category
from rest_framework import serializers
# from apps.api.serializers import UserPublicSerializer


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Doctors and Patients
    """
    class Meta:
        model = Category
        fields = ['id','name','description']


    
class CategoryDirectorSerializer(serializers.ModelSerializer):
    # TODO field with count of visits per category etc..
    """
    Serializer for creating Category
    """
    class Meta:
        model = Category
        fields = ['id','name','description']
        

    # def perform_create(self, validated_data):
    #     category = Category.objects.create(
    #         validated_data['name'], 
    #         validated_data['description'])
    #     category.name = validated_data['name']
    #     category.description = validated_data['description']
    #     # category.is_valid() # checks
    #     category.save()
    #     return category
    