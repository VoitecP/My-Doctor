from apps.core.models import User
from rest_framework import serializers

class LoginUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'password')



class UserPublicSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        # fields = '__all__'

        
class UserRegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'