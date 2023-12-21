from apps.core.models import Doctor
from rest_framework import serializers

from rest_framework.reverse import reverse

# from apps.api.serializers import UserPublicSerializer, UserPrivateSerializer, UserVisitSerializer
from apps.api.serializers import user_serializers
from apps.api.serializers.serializer_mixins import MappingMixin


class MixinModelSerializer(MappingMixin, serializers.ModelSerializer):    
    pass


class DoctorDynamicSerializer(MixinModelSerializer):

    # Fields for 'List' , 'create'
    get_full_name=serializers.CharField(label='Full Name', source='full_name', read_only=True)
    get_url=serializers.SerializerMethodField()

    # Fields for 'retrieve' , 'destroy', 
    get_first_name=serializers.CharField(label='First Name', source='user.first_name', read_only=True)
    get_last_name=serializers.CharField(label='Last Name', source='user.last_name', read_only=True)
    get_email=serializers.CharField(label='Email', source='user.email', read_only=True)
    get_specialization = serializers.CharField(label='Specialization', source='specialization', read_only=True)
    # Private fields
    get_phone = serializers.CharField(label='Phone', source='phone', read_only=True)
    get_private_field = serializers.CharField(label='Private Field', source='private_field', read_only=True)
    
    # Fields for 'update' , 'partial_update'
    first_name=serializers.CharField(source='user.first_name', max_length=150, default='', allow_blank=True)
    last_name=serializers.CharField(source='user.last_name',  max_length=150, default='', allow_blank=True)
    email=serializers.CharField(source='user.email', max_length=100, default='', allow_blank=True)
    phone=serializers.CharField(max_length=100, default='', allow_blank=True)
    specialization=serializers.CharField(max_length=100, default='', allow_blank=True)
    private_field=serializers.CharField(max_length=100, default='', allow_blank=True)

    mapping={
        'get_full_name':'Full Name',
        'get_url':'Link',
        #
        'get_first_name':'First Name',
        'get_last_name':'Last Name',
        'get_email':'Email',
        'get_specialization':'Specialization',
        'get_phone':'Phone',
        'get_private_field':'Private Field',
    }

    class Meta:
        model = Doctor
        fields = '__all__'


    def __init__(self, *args, **kwargs):
        context = kwargs.get('context', {})
        action = context.get('action')
        instance = context.get('instance', None)
        request_user = context['request'].user

        if action in ['list','create']:

            fields = ['get_full_name','get_url']
    
        if action in ['retrieve','destroy']:
            if (instance is not None and instance.user == request_user):

                fields = ['get_first_name','get_last_name',
                          'get_email','get_specialization', 
                          'get_phone','get_private_field']
            else:
                fields = ['get_first_name', 'get_last_name',
                          'get_email','get_specialization']

        if action in ['update','partial_update']:
            if (instance is not None and instance.user == request_user):

                fields = ['first_name','last_name','email','phone',
                        'specialization','private_field']
            
            else:
                fields = []
    
        super().__init__(*args, **kwargs)
    
        dynamic = set(fields)
        all_fields = set(self.fields)
        for field_pop in all_fields - dynamic:
            self.fields.pop(field_pop)

    def get_get_url(self, obj):
        request=self.context.get('request')
        if request is None:
            return None
        return reverse('api:doctor-detail', kwargs={'pk': obj.pk}, request=request)
    

## Junk serializers   

class DoctorPublicSerializer(serializers.ModelSerializer):
    """
    All users can view this fields
    """
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    user = user_serializers.UserPublicSerializer(read_only=True)
    
    class Meta:
        model = Doctor
        fields = ['user','specialization','tracks']
        # fields = '__all__'
         

class DoctorPrivateSerializer(serializers.ModelSerializer):
    """
    Only logged user can view these fields , self fields.
    """
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    user = user_serializers.UserPrivateSerializer(read_only=True)
    
    class Meta:
        model = Doctor
        fields = ['user','specialization','private_field','tracks']


class DoctorVisitSerializer(serializers.ModelSerializer):
    """
    Only connected thru common visit can see these fields
    """

    first_name=serializers.SerializerMethodField(label='first name', read_only=True)
    last_name=serializers.SerializerMethodField(label='last name', read_only=True)
    email=serializers.SerializerMethodField(read_only=True)
    #url=

    
    class Meta:
        model = Doctor
        fields = ['first_name','last_name', 'email','specialization']

    # def get_url(self, obj):
    #     return obj.url
    
    def get_first_name(self, obj):
        return obj.user.first_name
    
    def get_last_name(self, obj):
        return obj.user.last_name
    
    def get_email(self, obj):
        return obj.user.email



    







class DoctorUpdateSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Doctor
        fields = ['tracks','specialization', 'private_field','phone']
        # fields = '__all__'



