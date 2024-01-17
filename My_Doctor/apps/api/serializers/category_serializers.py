from rest_framework import serializers
from .serializer_mixins import DynamicModelSerializer, reverse_url

from apps.core.models import Category


# TODO CAtegory serializers

class CategoryDynamicSerializer(DynamicModelSerializer):
    # 
    get_url = serializers.SerializerMethodField()
    get_name = serializers.SerializerMethodField()
    get_description = serializers.SerializerMethodField()
    get_related_visit_count = serializers.SerializerMethodField()
    # 
    name = serializers.CharField(label='Name', max_length=100, min_length=3)
    description = serializers.CharField(label='Description', max_length=1000, min_length=10)
    
    mapping = {  
        'get_url':'Link',
        'get_name':'Name',
        'get_description':'Description',
        'get_related_visit_count':'Related visits',
    }

    class Meta:
        model = Category
        fields = '__all__'
        extra_kwargs =  {
                        'name': {'write_only': True},
                        'description': {'write_only': True},
                        }

    def get_dynamic_fields(self, instance, action, request_user):
        fields = []

        if action == 'list':
            if (request_user.is_staff or 
                request_user.usertype == 'c'):

                fields = ['get_url','get_name',
                          'get_related_visit_count']
            fields = ['get_url','get_name']

        if action == 'create':
            if (request_user.is_staff or 
                request_user.usertype == 'c'):

                fields = ['name','description']
            fields = []

        if action in ['retrieve','destroy']:
            if (request_user.is_staff  or 
                request_user.usertype == 'c'):
            
                fields = ['get_name','get_description',
                          'get_related_visit_count']
            fields = ['get_name','get_description']

        if action in ['update','partial_update']:
            if (request_user.is_staff  or 
                request_user.usertype == 'c'):
            
                fields = ['name','description']
            fields = []

        return fields


    # def get_get_url(self, obj):
    #     request=self.context.get('request')
    #     class_name = self.Meta.model.__name__.lower()
    #     if not request:
    #         return None
    #     return reverse(f'api:{class_name}-detail', kwargs={"pk": obj.pk}, request=request)

    def get_get_url(self, obj):
        return reverse_url(self, obj)
    
    def get_get_name(self, obj):
        return ''
    
    def get_get_description(self, obj):

        return ''
    
    def get_get_related_visit_count(self, obj):
        return '- related visits'
    
    
####
        
class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Doctors and Patients
    """
    class Meta:
        model = Category
        fields = ['id','name','description']


    
class CategoryDirectorSerializer(serializers.ModelSerializer):
    # TODO field with count of visits per category etc..
    """
    Serializer for creating Category
    """
    class Meta:
        model = Category
        fields = ['id','name','description']
        

    # def perform_create(self, validated_data):
    #     category = Category.objects.create(
    #         validated_data['name'], 
    #         validated_data['description'])
    #     category.name = validated_data['name']
    #     category.description = validated_data['description']
    #     # category.is_valid() # checks
    #     category.save()
    #     return category
    