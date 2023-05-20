from apps.core.models import User, Patient
from rest_framework import serializers


class LoginUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'password']


class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        # fields = '__all__'

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
        user.save()
        return user


# class UserRegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'first_name', 'last_name', 'usertype' ,'email', 'password']
#         extra_kwargs = {'password': {'write_only': True}}

#     # user_role=serializers.SerializerMethodField()

#     def create(self, validated_data):
#         user = User.objects.create_user(
#             validated_data['username'], 
#             validated_data['email'], 
#             validated_data['password'])
#         user.first_name = validated_data['first_name']
#         user.last_name = validated_data['last_name']
#         user.usertype = validated_data['usertype']
#         user.save()
#         return user

#     # def get_user_role(self, validated_data):
#     #     if validated_data['usertype'] == 'p':
#     #         return
#     #     if validated_data['usertype'] == 'd':
#     #         return