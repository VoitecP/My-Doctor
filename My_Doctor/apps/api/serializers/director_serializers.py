from apps.core.models import Director

from rest_framework import serializers
from rest_framework.response import Response 
from rest_framework.serializers import ValidationError

from apps.api.serializers import  user_serializers


class DirectorPublicSerializer(serializers.ModelSerializer):
    """
    All patient's and doctor's can see 
    """
    first_name=serializers.SerializerMethodField(label='first name', read_only=True)
    last_name=serializers.SerializerMethodField(label='last name', read_only=True)
    description=serializers.CharField(label='About Me', read_only=True)
   

    class Meta:
        model = Director
        # fields = '__all__'
        fields = ['first_name','last_name','description']

    
    def get_first_name(self, obj):
        return obj.user.first_name
    
    def get_last_name(self, obj):
        return obj.user.last_name
    



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


class DirectorDeleteSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Director
        fields = '__all__'


class DirectorCreateSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Director
        fields = '__all__'

    def perform_create(self, validated_data):
        try:
            director = Director.objects.create(
            validated_data['user'], 
            validated_data['phone'], 
            validated_data['description'])
            director.user = validated_data['user']
            director.phone = validated_data['phone']
            director.description = validated_data['decription']
            director.save()
            return director
        except:
            raise ValidationError({"detail": "Operation not allowed"})

