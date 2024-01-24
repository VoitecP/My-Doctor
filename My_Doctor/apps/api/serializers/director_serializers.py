from rest_framework import serializers

from apps.core.models import Director, User
from ..serializers.serializer_mixins import DynamicModelSerializer, reverse_url


class DirectorDynamicSerializerForPerson(DynamicModelSerializer):
    # Fields for 'List' , 'create'
    get_full_name=serializers.CharField(label='Full Name',source='full_name', read_only=True)
    get_url=serializers.SerializerMethodField()
    # Fields for 'retrieve' , 'destroy', 'update' , 'partial_update'
    get_first_name=serializers.CharField(label='First Name', source='user.first_name', read_only=True)
    get_last_name=serializers.CharField(label='Last Name', source='user.first_name', read_only=True)
    get_description=serializers.CharField(label='Description', source='description', read_only=True)
    
    mapping={
        'get_full_name':'Full Name',
        'get_url':'Link',
        'description':'Description',
        'get_first_name': 'First Name',
        'get_last_name': 'Last Name',
        'get_description': 'Description',
        }
    
    class Meta:
        model= Director
        fields='__all__'


    def get_dynamic_fields(self, instance, custom_action, request_user):
        fields = set()

        if custom_action in ['list','create']:
            fields = {'get_full_name','get_url'}
        
        elif custom_action in ['retrieve','destroy','update','partial_update']:
            fields = {'get_first_name', 'get_last_name','get_description'}
        return fields


    def get_get_url(self, obj):
        return reverse_url(self, obj)


class DirectorDynamicSerializerForDirector(DynamicModelSerializer):
    # Fields for 'List' , 'create'
    get_full_name = serializers.CharField(label='Full Name',source='full_name', read_only=True)
    get_url = serializers.SerializerMethodField()
    # Fields for 'retrieve' , 'destroy'
    get_first_name = serializers.CharField(label='First Name', source='user.first_name', read_only=True)
    get_last_name = serializers.CharField(label='Last Name', source='user.first_name', read_only=True)
    get_email = serializers.CharField(label='Email', source='user.email', read_only=True)
    get_phone = serializers.CharField(label='Phone', source='phone', read_only=True)
    get_description = serializers.CharField(label='Description', source='description', read_only=True)
    get_private_info = serializers.CharField(label='Personal Info', source='private_info', read_only=True)
    # Fields for  'update','partial_update'
   
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    first_name = serializers.CharField(source='user.first_name', max_length=150, default='', allow_blank=True)
    last_name = serializers.CharField(source='user.last_name',  max_length=150, default='', allow_blank=True)
    email = serializers.CharField(source='user.email', max_length=100, default='', allow_blank=True)
    phone = serializers.CharField(max_length=10, default='', allow_blank=True)

    mapping={
        'get_full_name':'Full Name',
        'get_url':'Link',
        #
        'get_first_name':'First Name',
        'get_last_name':'Last Name',
        'get_email':'Email',
        'get_phone':'Phone',
        'get_description':'Description',
        'get_private_info':'Personal Info',
    }

    class Meta:
        model = Director
        fields = '__all__'
        extra_kwargs =  {
            'user': {'write_only': True},
            'first_name': {'write_only': True},
            'last_name': {'write_only': True},
            'email': {'write_only': True},
            'phone': {'write_only': True},
            'description': {'write_only': True},
            'private_info': {'write_only': True},
        }


    def get_dynamic_fields(self, instance, custom_action, request_user):
        fields = set()

        if custom_action in ['list','create']:
            fields = {'get_full_name','get_url'}
        
        if custom_action in ['retrieve','destroy']:
            fields = {
                'get_first_name', 'get_last_name','get_email',
                'get_phone','get_description','get_private_info'
            }    

        if custom_action in ['update','partial_update']:
            fields = {
                'user','first_name','last_name',
                'email','phone','description','private_info'
            }
        return fields
    
    
    def get_get_url(self, obj):
        return reverse_url(self, obj)


    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        first_name = user_data.get('first_name', instance.user.first_name)
        last_name = user_data.get('last_name', instance.user.last_name)
        email = user_data.get('email', instance.user.email)
        user_def = {
            'first_name': first_name,
            'last_name': last_name,
            'email':email,
        }
        User.objects.update_or_create(id=instance.user.id, defaults=user_def)

        phone = validated_data.get('phone', instance.phone)
        description = validated_data.get('description', instance.description)
        private_info = validated_data.get('private_info', instance.private_info)
        director_def = {
            'phone': phone,
            'description': description,
            'private_info': private_info,
        }
        director, created = Director.objects.update_or_create(user=instance.user, 
                                                              defaults=director_def)
        return director

 
