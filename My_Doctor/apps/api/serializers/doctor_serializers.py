from rest_framework import serializers

from ..serializers.serializer_mixins import DynamicModelSerializer, reverse_url
from apps.core.models import Doctor, User


class DoctorDynamicSerializer(DynamicModelSerializer):

    ## Fields for 'List' , 'create'
    get_full_name=serializers.CharField(label='Full Name', source='full_name', read_only=True)
    get_url=serializers.SerializerMethodField()

    ## Fields for 'retrieve' , 'destroy', 
    get_first_name=serializers.CharField(label='First Name', source='user.first_name', read_only=True)
    get_last_name=serializers.CharField(label='Last Name', source='user.last_name', read_only=True)
    get_specialization = serializers.CharField(label='Specialization', source='specialization', read_only=True)
    # Visit related fields
    get_email=serializers.CharField(label='Email', source='user.email', read_only=True)
    # Private fields
    get_phone = serializers.CharField(label='Phone', source='phone', read_only=True)
    get_private_field = serializers.CharField(label='Private Field', source='private_field', read_only=True)
    
    ## Fields for 'update' , 'partial_update'
    first_name=serializers.CharField(source='user.first_name', max_length=150, default='', allow_blank=True)
    last_name=serializers.CharField(source='user.last_name',  max_length=150, default='', allow_blank=True)
    email=serializers.CharField(source='user.email', max_length=100, default='', allow_blank=True)
    phone=serializers.CharField(max_length=100, default='', allow_blank=True)
    specialization=serializers.CharField(max_length=100, default='', allow_blank=True)
    private_field=serializers.CharField(max_length=100, default='', allow_blank=True)

    mapping={
        'get_full_name':'Full Name',
        'get_url':'Link',
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
        extra_kwargs =  {
            'first_name': {'write_only': True},
            'last_name': {'write_only': True},
            'email': {'write_only': True},
            'phone': {'write_only': True},
            'specialization': {'write_only': True},
            'private_field': {'write_only': True},
        }

    def get_dynamic_fields(self, instance, custom_action, request_user):
        fields = set()
        owner = bool(instance is not None 
                and (instance.user == request_user or request_user.is_staff))
        
        if custom_action in ['list','create']:
            fields = {'get_full_name','get_url'}
    
        elif custom_action in ['retrieve','destroy']:
            if owner:
                fields = {'get_first_name','get_last_name',
                          'get_email','get_specialization', 
                          'get_phone','get_private_field'}
            else:
                fields = {'get_first_name', 'get_last_name',
                          'get_specialization'
}
        elif custom_action in ['update','partial_update']:
            if owner:
                fields = {'first_name','last_name','email','phone',
                        'specialization','private_field'}
            else:
                fields = {'first_name'}
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
        specialization = validated_data.get('specialization', instance.specialization)
        private_field = validated_data.get('private_field', instance.private_field)
        doctor_def = {
            'phone': phone,
            'specializaion': specialization,
            'private_field': private_field,
        }
        doctor, created = Doctor.objects.update_or_create(user=instance.user, 
                                                              defaults=doctor_def)
        return doctor