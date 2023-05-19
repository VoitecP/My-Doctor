from apps.core.models import User, Patient
from rest_framework import serializers
# from .patient_serializers import PatientUpdateSerializer

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


# class Patient2UpdateSerializer(serializers.ModelSerializer):
#     tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
#     class Meta:
#         model = Patient
#         # fields = '__all__'
#         fields = ['tracks','adress', 'birth_date','phone']
#         # ields = ['tracks', 'user','adress', 'birth_date','phone']
#         # extra_kwargs = {'password': {'write_only': True}}
#         extra_kwargs = {'user': {'default': serializers.CurrentUserDefault()}}

#     def create(self, validated_data):
        
      
        
#         patient = Patient()
#         # patient.user = validated_data.get['user']
#         patient.adress = validated_data['adress']
#         patient.birth_date = validated_data['birth_date']
#         patient.phone = validated_data['phone']
#         patient.save()
#         return patient




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



class User2RegisterSerializer(serializers.ModelSerializer):

    user_role=serializers.SerializerMethodField()

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

    def get_user_role(self, validated_data):

        if validated_data['usertype'] == 'p':
            return
            
        if validated_data['usertype'] == 'd':
            return