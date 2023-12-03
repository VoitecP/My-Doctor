from apps.core.models import Director, User

from rest_framework.permissions import SAFE_METHODS
from rest_framework import serializers
from rest_framework.response import Response 
from rest_framework.serializers import ValidationError

from apps.api.serializers import  user_serializers
from apps.api.serializers.serializer_mixins import MappingMixin
from rest_framework.reverse import reverse


class MixinModelSerializer(MappingMixin, serializers.ModelSerializer,):
    
    pass


class DirectorListSerializer(MixinModelSerializer):
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
 

# todo connect serializers  List and Retrieve for person
class DirectorRetrieveSerializerForPerson(MixinModelSerializer):
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


# class DirectorRetrieveSerializerForDirector(MixinModelSerializer):

#     first_name=serializers.CharField(label='First Name', source='user.first_name', read_only=True)
#     last_name=serializers.CharField(label='Last Name', source='user.first_name', read_only=True)
#     email=serializers.CharField(label='Email', source='user.email')

class DirectorUpdateSerializerForDirector(MixinModelSerializer):

    # Fields for 'List' , 'create'
    fields_list=[
        'url','full_name'
        ]
    url=serializers.SerializerMethodField()
    full_name=serializers.CharField(label='Full Name', read_only=True)

    # Fields for 'retrieve' , 'destroy'
    fields_retrieve=[
        'first_name_r', 'last_name_r','email_r','phone_r','description_r','private_info_r'
        ]
    first_name_r=serializers.CharField(label='First Name', source='user.first_name', read_only=True)
    last_name_r=serializers.CharField(label='Last Name', source='user.first_name', read_only=True)
    email_r=serializers.CharField(label='Email', source='user.email', read_only=True)
    phone_r=serializers.CharField(label='Phone', source='phone', read_only=True)
    description_r=serializers.CharField(label='Description', source='description', read_only=True)
    private_info_r=serializers.CharField(label='Personal Info', source='private_info', read_only=True)

    # Fields for  'update','partial_update'
    fields_update=[
        'user','first_name','last_name','email','phone','description','private_info'
        ]
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    first_name=serializers.CharField(label='First Name', source='user.first_name', max_length=150, default='', allow_blank=True)
    last_name=serializers.CharField(source='user.last_name',  max_length=150, default='', allow_blank=True)
    email=serializers.CharField(source='user.email', max_length=100, default='', allow_blank=True)
    # phone
    # description
    # private_info
 
    # pop_fields=['user']
    # mapping={
    #     'first_name':'First Name',
    #     'last_name':'Last Name',
    #     'email':'Email',
    #     'phone':'Phone',
    #     'description':'Description',
    #     'private_info':'Personal Info',

    # }

    class Meta:
        model= Director
        fields='__all__'

    def get_url(self, obj):
        request=self.context.get('request')
        if request is None:
            return None
        return reverse('api:director-detail', kwargs={"pk": obj.pk}, request=request)
    

    ### Serializer Methods ###

    def get_fields(self):
        fields = super().get_fields()
        action = self.context.get('action')

        if action in ['list','create']:
            exclude = ['slug'] + self.fields_list + self.fields_update
            for field in exclude:
                fields.pop(field, None)
            return fields

        if action in ['retrieve', 'destroy']: 
            exclude = ['slug'] + self.fields_list + self.fields_update
            for field in exclude:
                fields.pop(field, None)
            return fields
        
        if action in ['update','partial_update']:
            exclude = ['slug'] + self.fields_list + self.fields_retrieve
            for field in exclude:
                fields.pop(field, None)
            return fields

    
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
            'phone':phone,
            'description': description,
            'private_info': private_info,
        }
        director, created = Director.objects.update_or_create(user=instance.user, 
                                                              defaults=director_def)
        return director



        # if action == ['retrieve']:
        #     # Zmieniamy zestaw pól dla akcji list
        #     # exclude = ['user',
        #     #            'first_name',
        #     #            'last_name',
        #     #            #'email',
        #     #            'phone',
        #     #            'description',
        #     #            'private_info',
        #     #            ]
        #     # for field in exclude:
        #     #     fields.pop(field, None)
        # # elif request and request.method == 'GET' and 'pk' in self.context:
        # #     # Zmieniamy zestaw pól dla akcji retrieve
        # #     fields_to_exclude = ['another_field_to_exclude']
        # #     for field in fields_to_exclude:
        # #         fields.pop(field, None)
        #     print(fields)
        #     return fields
####
# Other Serializers Not Need now
#  TODO something not working
class DirectorUpdateSerializer:

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


