from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# Removed
# from dj_rest_auth.serializers import UserDetailsSerializer
# from dj_rest_auth.registration.serializers import RegisterSerializer

from .serializer_mixins import  DynamicModelSerializer, reverse_url
from apps.core.models import Director, User

class UserDynamicSerializer(DynamicModelSerializer):
    ## Fields for 'list' 
    get_full_name = serializers.SerializerMethodField()
    get_url = serializers.SerializerMethodField()
    ## Fields for 'retrieve' , 'destroy', 
    get_first_name = serializers.CharField(label='First Name', source='first_name', read_only=True)
    get_last_name = serializers.CharField(label='Last Name', source='last_name', read_only=True)
    # Private fields
    get_email = serializers.CharField(label='Email', source='email', read_only=True)
    get_username = serializers.CharField(label='User name', source='username', read_only=True)
    get_usertype = serializers.SerializerMethodField()
    get_date_created = serializers.DateTimeField(label='Date Created', source='date_joined', format='%d-%m-%Y %H:%M:%S', read_only=True)
    get_account_duration = serializers.SerializerMethodField()
    ## Fields for 'create'
    username = serializers.CharField(max_length=50, label='Username',
                validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(max_length=50, label='Password')
    change_password = serializers.CharField(label='Change Password',  max_length=50, required = False)
    first_name =  serializers.CharField(max_length=50, label='First Name')
    last_name =  serializers.CharField(max_length=50, label='Last Name')
    email =  serializers.EmailField(label='Email')
    usertype = serializers.ChoiceField(label='User Type', choices=[])

    mapping = {
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


    def get_dynamic_fields(self, instance, custom_action, request_user):
        fields = set()
        director = bool(request_user.is_staff or request_user.usertype == 'c')
        owner = bool(instance and instance == request_user)
        owner_or_staff = bool(instance and (instance == request_user
                                                or request_user.is_staff))
        
        create_fields = {'username','password',
                         'usertype','first_name',
                         'last_name','email'}
        retrieve_fields = {'get_username','get_first_name',
                          'get_last_name', 'get_email',
                          'get_usertype', 'get_date_created',
                          'get_account_duration'}
        
        if custom_action == 'list':
                fields = {'get_full_name','get_url'}

        elif custom_action == 'create':
            if director:
                    fields = create_fields
    
        elif custom_action in ['retrieve','destroy']: 
            if owner:
                    fields = retrieve_fields 
            else:
                    fields = {'get_first_name', 'get_last_name', 'get_usertype'}

        elif custom_action in ['update','partial_update']:
            if owner_or_staff:
                    fields = create_fields - {'usertype','password'} | {'change_password'}
                   
        return fields


    def perform_init(self, context):
        self.fields['usertype'].choices = self.get_usertype_choices()
        

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
        return (f'{years} years, '
                f'{months} months, '
                f'{days} days, '
                f'{hours} hours, '
                f'{minutes} minutes, '
                f'{seconds} seconds')
    
    def get_get_usertype(self, obj):
        return User.CHOICES.get(obj.usertype, 'Is Staff')
        
    def get_get_url(self, obj):
        return reverse_url(self, obj)
       
    def get_usertype_choices(self):
        choices = {
        'p':'Patient',
        'd': 'Doctor',
        'c': 'Director', 
        }
        if Director.objects.exists():
            choices.pop('c')
            return choices.items()
        return choices.items()
        
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
    

class UserManageDynamicSerializer(DynamicModelSerializer):
    #
    get_username = serializers.CharField(label='User name', source='username', read_only=True)
    get_first_name=serializers.CharField(label='First Name', source='first_name', read_only=True)
    get_last_name=serializers.CharField(label='Last Name', source='last_name', read_only=True)
    get_email=serializers.CharField(label='Email', source='email', read_only=True)
    get_usertype = serializers.SerializerMethodField()
    #
    username = serializers.CharField(max_length=50, label='Username',
                validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(max_length=50, label='Password')
    change_password = serializers.CharField(label='Change Password',  max_length=50, required = False)
    first_name =  serializers.CharField(max_length=50, label='First Name')
    last_name =  serializers.CharField(max_length=50, label='Last Name')
    email =  serializers.EmailField(label='Email')
    usertype = serializers.ChoiceField(label='User Type', choices=[])
    pop_fields = {'password'}

    mapping = {
            'get_username': 'Username',
            'get_first_name':'First Name',
            'get_last_name':'Last Name',
            'get_email':'Email',
            'get_usertype':'User Type',
            #
            # 'username': 'Username',
            # 'first_name':'First Name',
            # 'last_name':'Last Name',
            # 'email':'Email',
            # 'usertype':'User Type',
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

    def perform_init(self, context):
        self.fields['usertype'].choices = self.get_usertype_choices()
        

    def perform_to_representation(self, serializer):
        key = serializer.get('usertype', None)
        if key:
            value = self.fields['usertype'].choices.get(key, None)
            serializer['usertype'] = value
        return serializer
    

    def get_dynamic_fields(self, instance, custom_action, request_user):
        fields = set()
        owner = bool(instance == request_user)
        create_fields = {'username','password',
                         'usertype','first_name',
                         'last_name','email'}
        retrieve_fields = {'get_username','get_first_name',
                          'get_last_name', 'get_email',
                          'get_usertype', 'get_date_created',
                          'get_account_duration'}
        if custom_action == 'create':
            if not request_user.is_authenticated:
                fields = create_fields
    
        elif custom_action in ['retrieve','destroy']:
            if owner:
                fields = retrieve_fields

        elif custom_action in ['update','partial_update']:
            if owner:
                fields = create_fields - {'usertype','password'} | {'change_password'}          
        
        return fields


    def get_usertype_choices(self):
        choices = {
        'p':'Patient',
        'd': 'Doctor',
        'c': 'Director', 
        }
        if Director.objects.exists():
            choices.pop('c')
            return choices.items()
        return choices.items()
    

    def get_get_usertype(self, obj):
        return User.CHOICES.get(obj.usertype, 'Is Staff')


    def create(self, validated_data):
        user = User()
        user.username = validated_data['username']
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.email=  validated_data['email']  
        user.usertype = validated_data['usertype']
        user.set_password(validated_data['password'])
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


# Todo for DRF-Auth
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
    
    



    





    
    
