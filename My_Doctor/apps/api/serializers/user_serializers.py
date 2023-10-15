from apps.core.models import User, Patient

from rest_framework import serializers

from dj_rest_auth.serializers import UserDetailsSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer


class UserPublicSerializer(serializers.ModelSerializer):
    """
    All users can view this fields
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        # fields = '__all__'


class UserPrivateSerializer(serializers.ModelSerializer):
    """
    Only logged user can view these fields , self fields.
    """
    class Meta:
        model = User
        # fields = '__all__'
        fields = ['id','first_name', 'last_name', 'email','usertype']


class UserVisitSerializer(serializers.ModelSerializer):
    '''
    Serializer for doctor/ related visit view
    '''
    class Meta:
        model = User
        # fields = '__all__'
        # Dynamic field serializer ??
        fields = ['first_name', 'last_name', 'email']


###

class LoginUserSerializer(serializers.ModelSerializer):
    """
    Serializer for login
    """
    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'password']


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for update user fields
    """
    class Meta:
        model = User
        # fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}
        fields = ['first_name', 'last_name', 'email']





class DeleteUserSerializer(serializers.ModelSerializer):
    """
    Serializer for delete user
    """
    class Meta:
        model = User
        fields = '__all__'





class CustomUserRegisterSerializer(RegisterSerializer, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','usertype','password1', 'password2']

    def custom_signup(self, request, user):
        user.username = self.validated_data['username']
        user.email = self.validated_data['email']
        user.usertype = self.validated_data['usertype']
        user.password1 = self.validated_data['password1']
        user.password2 = self.validated_data['password2']
        user.save()
        return user



class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for register user
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'usertype' ,'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def perform_create(self, validated_data):
        user = User.objects.create(
            validated_data['username'], 
            validated_data['email'], 
            validated_data['password'])
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.usertype = validated_data['usertype']
        # user.is_valid() # checks
        user.save()
        return user


