
from rest_framework import serializers

from ..serializers.serializer_mixins import  DynamicModelSerializer, reverse_url
from apps.core.models import Patient, User


class PatientDynamicSerializer(DynamicModelSerializer):
    ## Fields for 'List' , 'create'
    get_full_name=serializers.CharField(label='Full Name', source='full_name', read_only=True)
    get_url=serializers.SerializerMethodField()

    ## Fields for 'retrieve' , 'destroy', 
    get_first_name=serializers.CharField(label='First Name', source='user.first_name', read_only=True)
    get_last_name=serializers.CharField(label='Last Name', source='user.last_name', read_only=True)
    get_birth_date = serializers.DateField(label='Birth Date', source='birth_date', read_only=True)
    # Visit related fields
    get_email=serializers.CharField(label='Email', source='user.email', read_only=True)
    # Private fields
    get_phone = serializers.CharField(label='Phone', source='phone', read_only=True)
    get_adress = serializers.CharField(label='Adress', source='adress', read_only=True)
      
    ## Fields for 'update' , 'partial_update'
    first_name=serializers.CharField(source='user.first_name', max_length=150, default='', allow_blank=True)
    last_name=serializers.CharField(source='user.last_name',  max_length=150, default='', allow_blank=True)
    birth_date=serializers.DateField(default='')
    # TODO Phone field update
    email = serializers.CharField(source='user.email', max_length=100, default='', allow_blank=True)
    phone = serializers.CharField(max_length=10, default='', allow_blank=True)
    adress = serializers.CharField(max_length=100, default='', allow_blank=True)
    
    mapping={
        'get_full_name':'Full Name',
        'get_url':'Link',
        #
        'get_first_name':'First Name',
        'get_last_name':'Last Name',
        'get_email':'Email',
        'get_birth_date':'Birth Date',
        'get_phone':'Phone',
        'get_adress':'Adress',     
    }

    class Meta:
        model = Patient
        fields = '__all__'
        extra_kwargs =  {
            'first_name': {'write_only': True},
            'last_name': {'write_only': True},
            'birth_date': {'write_only': True},
            'email': {'write_only': True},
            'phone': {'write_only': True},
            'adress': {'write_only': True},
            'private_field': {'write_only': True},
        }


    def get_dynamic_fields(self, instance, custom_action, request_user):
        fields = set()
        owner = bool(instance and instance.user == request_user)
        retrieve_fields = {'get_first_name','get_last_name',
                          'get_birth_date','get_email', 
                          'get_phone','get_adress'}
        update_fields = {'first_name','last_name',
                         'birth_date','email',
                         'phone','adress'}
        
        if custom_action in ['list','create']:
            fields = {'get_full_name','get_url'}
    
        elif custom_action in ['retrieve','destroy']:
            if owner:
                fields = retrieve_fields
            else:
                fields = retrieve_fields - {'get_email','get_phone','get_adress'}

        elif custom_action in ['update','partial_update']:
            if owner:
                fields = update_fields
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
        birth_date = validated_data.get('birth_date', instance.birth_date)
        adress = validated_data.get('adress', instance.adress)
        patient_def = {
            'phone': phone,
            'birth_date': birth_date,
            'adress': adress,
        }
        patient, created = Patient.objects.update_or_create(user=instance.user, 
                                                              defaults=patient_def)
        return patient
