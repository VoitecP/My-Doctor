from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework.serializers import ValidationError

from apps.core.models import Director, User
from .serializer_mixins import MappingModelSerializer, DynamicModelSerializer, reverse_url

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
    get_full_name=serializers.CharField(label='Full Name',source='full_name', read_only=True)
    get_url=serializers.SerializerMethodField()

    # Fields for 'retrieve' , 'destroy'
    get_first_name=serializers.CharField(label='First Name', source='user.first_name', read_only=True)
    get_last_name=serializers.CharField(label='Last Name', source='user.first_name', read_only=True)
    get_email=serializers.CharField(label='Email', source='user.email', read_only=True)
    get_phone=serializers.CharField(label='Phone', source='phone', read_only=True)
    get_description=serializers.CharField(label='Description', source='description', read_only=True)
    get_private_info=serializers.CharField(label='Personal Info', source='private_info', read_only=True)
    
    # Fields for  'update','partial_update'
    # Todo replace user for user link:
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    first_name=serializers.CharField(source='user.first_name', max_length=150, default='', allow_blank=True)
    last_name=serializers.CharField(source='user.last_name',  max_length=150, default='', allow_blank=True)
    email=serializers.CharField(source='user.email', max_length=100, default='', allow_blank=True)
    # phone   - heritated from Person/Director model
    # description
    # private_info

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
        email=user_data.get('email', instance.user.email)
        user_def={
            'first_name': first_name,
            'last_name': last_name,
            'email':email,
        }
        User.objects.update_or_create(id=instance.user.id, defaults=user_def)

        phone=validated_data.get('phone', instance.phone)
        description = validated_data.get('description', instance.description)
        private_info = validated_data.get('private_info', instance.private_info)
        director_def={
            'phone': phone,
            'description': description,
            'private_info': private_info,
        }
        director, created = Director.objects.update_or_create(user=instance.user, 
                                                              defaults=director_def)
        return director


### Other serializers junk
class DirectorUpdateSerializer:
# todo something not working , remove this plug
    pass 

class DirectorCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Director
        fields = '__all__'

    def perform_create(self, validated_data):
        try:
            director = Director.objects.create(
            validated_data['user'], 
            validated_data['phone'], 
            validated_data['description'])
            director.user = validated_data['user']
            director.phone = validated_data['phone']
            director.description = validated_data['decription']
            director.save()
            return director
        except:
            raise ValidationError({"detail": "Operation not allowed"})




class DirectorListSerializer(MappingModelSerializer):
    url=serializers.SerializerMethodField()
    full_name=serializers.SerializerMethodField()

    mapping={
        'url': 'Link',
        'full_name': 'Full Name',
    }

    class Meta:
        model = Director
        fields=['url', 'full_name']

        
    def get_url(self, obj):
        request=self.context.get('request')

        # Todo dynamic Serializers
        # usertype=request.user.usertype
        # return usertype
        # action=self.context.get('action')
        # return action
        if request is None:
            return None
        return reverse('api:director-detail', kwargs={"pk": obj.pk}, request=request)
        
    def get_full_name(self, obj):
        return obj.full_name    
 


class DirectorRetrieveSerializerForPerson(MappingModelSerializer):

    full_name=serializers.SerializerMethodField()
    phone=serializers.SerializerMethodField()
    description=serializers.SerializerMethodField()

    mapping={
        'full_name':'Full Name',
        'phone':'Phone',
        'description':'Description',
    }
    class Meta:
        model = Director
        fields = ['full_name','m_phone','description']

    def get_full_name(self, obj):
        return obj.full_name

    def get_m_phone(self, obj):
        return obj.phone

    def get_m_description(self, obj):
        return obj.description