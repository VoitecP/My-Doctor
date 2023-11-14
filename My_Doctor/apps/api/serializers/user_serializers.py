from apps.core.models import User, Patient

from rest_framework import serializers

# Removed
# from dj_rest_auth.serializers import UserDetailsSerializer
# from dj_rest_auth.registration.serializers import RegisterSerializer


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


# for DRF-auth
# # class CustomUserRegisterSerializer(RegisterSerializer, serializers.ModelSerializer):
# class CustomUserRegisterSerializer(serializers.ModelSerializer):
#     """
#     Serializer for Register User, mixin with dj_rest_auth app
#     """

#     class Meta:
#         model = User
#         fields = ['username','email','usertype','password']

#     def custom_signup(self, request, user):
#         user.username = self.validated_data['username']
#         user.email = self.validated_data['email']
#         user.usertype = self.validated_data['usertype']
#         user.password = self.validated_data['password']
#         user.password2 = self.validated_data['password2']
#         user.save()
#         return user
    
    


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for register user
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 
                  'last_name', 'usertype' ,'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User()
        user.username = validated_data['username']
        user.email=  validated_data['email']
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.usertype = validated_data['usertype']
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    # def create(self, validated_data):
    #     user = User.objects.create(
    #         username=validated_data['username']
    #     )
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user


    # def create(self, validated_data):
    #     user = User(
    #         username=validated_data['username']
    #     )
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user

# lass CreateUser(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request, format='json'):
#         print(request.data)
#         data = request.data
#         reg_serializer = RegisterUserSerializer(data=data)
#         if reg_serializer.is_valid():
#             password = reg_serializer.validated_data.get('password')
#             reg_serializer.validated_data['password']=make_password(password)
#             new_user = reg_serializer.save()
#             if new_user:
#                 return Response(status=status.HTTP_201_CREATED)
#         return Response(reg_serializer.errors,status=status.HTTP_400_BAD_REQUEST)



##

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        user = User(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


