from rest_framework import serializers

from ..serializers.serializer_mixins import DynamicModelSerializer, reverse_url
from apps.core.models import Category, Visit


class CategoryDynamicSerializer(DynamicModelSerializer):
    # 
    get_url = serializers.SerializerMethodField()
    get_name=serializers.CharField(label='Name', source='name', read_only=True)
    get_description=serializers.CharField(label='Name', source='description', read_only=True)
    get_related_visit_count = serializers.SerializerMethodField()
    # 
    name = serializers.CharField(label='Name', max_length=100, min_length=3)
    description = serializers.CharField(label='Description', max_length=1000, min_length=10)
    
    mapping = { 
        'get_name':'Name',
        'get_url':'Link',
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

    
    def get_dynamic_fields(self, instance, custom_action, request_user):
        fields = set()
        director = bool(request_user.is_staff or request_user.usertype == 'c')
        list_fields = {'get_url','get_name', 'get_related_visit_count'}
        retrieve_fields = {'get_name','get_description', 'get_related_visit_count'}
        
        if custom_action == 'list':
            if director:
                fields = list_fields
            else:
                fields = list_fields - {'get_related_visit_count'}

        elif custom_action == 'create':
            if director:
                fields = {'name','description'}

        elif custom_action in ['retrieve','destroy']:
            if director:
                fields = retrieve_fields
            else:
                fields = retrieve_fields - {'get_related_visit_count'}

        elif custom_action in ['update','partial_update']:
            if director:
                fields = {'name','description'}
        return fields


    def get_get_url(self, obj):
        return reverse_url(self, obj)
    
    
    def get_get_related_visit_count(self, obj):
        queryset = Visit.objects.filter(category=obj).count()
        return queryset
    
  