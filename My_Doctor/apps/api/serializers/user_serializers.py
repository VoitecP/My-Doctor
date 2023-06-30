from apps.core.models import User, Patient
from rest_framework import serializers


class UserPublicSerializer(serializers.ModelSerializer):
    '''
    Serializer for public view
    '''
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

        # fields = '__all__'


class UserPrivateSerializer(serializers.ModelSerializer):
    '''
    Serializer for private view
    '''
    class Meta:
        model = User
        fields = '__all__'


class UserVisitSerializer(serializers.ModelSerializer):
    '''
    Serializer for doctor/ related visit view
    '''
    class Meta:
        model = User
        fields = '__all__'


###

class LoginUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'password']


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}
        fields = ['first_name', 'last_name', 'email']


    # def update(self, validated_data):
    #     user = self.request.user
    #      User.objects.create_user(
    #         validated_data['username'], 
    #         validated_data['email'], 
    #         validated_data['password'])
    #     user.first_name = validated_data['first_name']
    #     user.last_name = validated_data['last_name']
    #     user.usertype = validated_data['usertype']
    #     # user.is_valid() # checks
    #     user.save()



class DeleteUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'usertype' ,'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'], 
            validated_data['email'], 
            validated_data['password'])
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.usertype = validated_data['usertype']
        # user.is_valid() # checks
        user.save()
        return user


