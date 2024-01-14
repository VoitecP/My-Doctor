from django.utils import timezone
from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework.validators import UniqueValidator

# Removed
# from dj_rest_auth.serializers import UserDetailsSerializer
# from dj_rest_auth.registration.serializers import RegisterSerializer

from apps.core.models import Director, User
from .serializer_mixins import MappingModelSerializer



class UserDynamicSerializer(MappingModelSerializer):

    ## Fields for 'List' 
    get_full_name = serializers.SerializerMethodField()
    get_url=serializers.SerializerMethodField()
    
    ## Fields for 'retrieve' , 'destroy', 
    get_first_name=serializers.CharField(label='First Name', source='first_name', read_only=True)
    get_last_name=serializers.CharField(label='Last Name', source='last_name', read_only=True)
    
    # Private fields
    get_email=serializers.CharField(label='Email', source='email', read_only=True)
    get_username = serializers.CharField(label='User name', source='username', read_only=True)
    get_usertype = serializers.SerializerMethodField()
    get_date_created=serializers.DateTimeField(label='Date Created', source='date_joined', format='%d-%m-%Y %H:%M:%S', read_only=True)
    get_account_duration=serializers.SerializerMethodField()

    ## Fields for 'Create'
    username = serializers.CharField(max_length=50, label='Username',
                validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(max_length=50, label='Password')
    change_password = serializers.CharField(label='Change Password',  max_length=50, required = False)
    first_name =  serializers.CharField(max_length=50, label='First Name')
    last_name =  serializers.CharField(max_length=50, label='Last Name')
    email =  serializers.CharField(label='Email')
    usertype = serializers.ChoiceField(label='User Type', choices=[])

    mapping={
        'get_full_name':'Full Name',
        'get_url':'Link',
        #
        'get_username': 'Username',
        'get_first_name':'First Name',
        'get_last_name':'Last Name',
        'get_email':'Email',
        'get_usertype':'User Type',
        'get_date_created':'Date Joined',
        'get_account_duration':'Account life span',
    }

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'username': {'write_only': True},
            'password': {'write_only': True},
            'change_password': {'write_only': True},
            'first_name': {'write_only': True},
            'last_name': {'write_only': True},
            'email': {'write_only': True},
        }


    def __init__(self, *args, **kwargs):
        context = kwargs.get('context', {})
        action = context.get('action')
        instance = context.get('instance', None)
        request_user = context['request'].user

        if action == 'list':
            fields = ['get_full_name','get_url']

        if action == 'create':
            if (request_user.is_staff == True or 
                request_user.usertype == 'c'):

                fields = ['username','password','usertype',
                          'first_name','last_name','email']
            
            else:
                fields = []
                # fields = ['firt_name']
    
        if action in ['retrieve','destroy']:
            if (instance is not None and instance == request_user):

                fields = ['get_username','get_first_name','get_last_name', 
                          'get_email','get_usertype', 'get_date_created',
                          'get_account_duration']
            else:
                fields = ['get_first_name', 'get_last_name', 'get_usertype']

        if action in ['update','partial_update']:
            if (instance is not None and instance == request_user):

                fields = ['username','change_password',
                          'first_name','last_name','email']
            else:
                fields = []
    
        super().__init__(*args, **kwargs)
        # self.fields['usertype'].choices = self.get_usertype_choices(*args, **kwargs)
        self.fields['usertype'].choices = self.get_usertype_choices()

        dynamic = set(fields)
        all_fields = set(self.fields)
        for field_pop in all_fields - dynamic:
            self.fields.pop(field_pop)

            
    def get_get_full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'


    def get_get_account_duration(self, obj):
        joined = obj.date_joined
        now = timezone.now()
        time_delta = now-joined

        years = now.year - joined.year
        months = now.month - joined.month
        days = time_delta.days
        hours, mod = divmod(time_delta.seconds, 3600)
        minutes, seconds = divmod(mod, 60)
        
        # return f'{days} :days, {hours} :hours, {minutes} :minutes, {seconds} :seconds'
        return f' {years} :years, {months} :months, {days} :days, {hours} :hours, {minutes} :minutes, {seconds} :seconds'


    def get_get_usertype(self, obj):
        if obj.usertype == 'p':
            return 'Patient'
        if obj.usertype == 'd':
            return 'Doctor'
        if obj.usertype == 'c':
            return 'Director'


    def get_get_url(self, obj):
        request=self.context.get('request')
        if request is None:
            return None
        return reverse('api:user-detail', kwargs={'pk': obj.pk}, request=request)
       

    def get_usertype_choices(self):

        if Director.objects.exists():
            choices = [
            ('p', 'Patient'),
            ('d', 'Doctor'),
            ]  
            return choices

        else:
            choices = [
            ('p', 'Patient'),
            ('d', 'Doctor'),
            ('c', 'Director'),
            ]
            return choices


    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     data.pop('change_password', None)
    #     return data
    
       
    def create(self, validated_data):
        user = User()
        user.username = validated_data['username']
        user.set_password(validated_data['password'])
        user.usertype = validated_data['usertype']
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.email = validated_data['email']
        user.save()

        return user


    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        
        change_password = validated_data.get('change_password', None)
        if change_password:
            instance.set_password(change_password)
        validated_data.pop('change_password', None)

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
    
        return instance
    

###  Junk serializers
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
        # TODO , if admin.is_staff  user.usertype= user.DIRECTOR or just another view for director.
        
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


