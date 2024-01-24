from rest_framework import serializers
from rest_framework.reverse import reverse

from ..serializers.serializer_mixins import MappingModelSerializer, DynamicModelSerializer, reverse_url
from apps.core.models import VisitImageFile, Visit

class VisitImageDynamicSerializer(DynamicModelSerializer):

    # Fields for 'List', 'Retrieve'
    get_visit_title = serializers.SerializerMethodField()
    get_visit_url = serializers.SerializerMethodField()
    get_visit_image_url = serializers.SerializerMethodField()
    get_image_url=serializers.SerializerMethodField()
    get_thumb_url=serializers.SerializerMethodField()
    # 'Fields for 'Create'
    visit = serializers.PrimaryKeyRelatedField(label='Visit', queryset=Visit.objects.all(), required=True)
    image = serializers.ImageField()
    
    mapping = {  
        'get_visit_title':'Visit Title',
        'get_visit_url':'Visit Link',
        'get_visit_image_url':'Visit Image',
        'get_image_url':'Image Link',
        'get_thumb_url':'Thumbnail Link',   
    }

    class Meta:
        model = VisitImageFile  
        fields = '__all__'
        extra_kwargs =  {
            'visit': {'write_only': True},
            'image': {'write_only': True},
        }        
        
  
    def get_dynamic_fields(self, instance, custom_action, request_user):
        fields = set()

        if custom_action == 'list':
            fields = {'get_visit_title','get_visit_image_url'}

        elif custom_action =='create':
            fields = {'image','visit'}

        elif custom_action in ['retrieve','destroy']:
            fields = {'get_visit_title', 'get_visit_url',
                      'get_image_url','get_thumb_url'}
        
        elif custom_action in {'update','partial_update'}:
            pass

        return fields
    

    def perform_init(self, context):
        request_user = getattr(context['request'], 'user', None)
        user_id = getattr(request_user, 'id', 'None')
        self.fields['visit'].queryset = Visit.objects.filter(patient_id=user_id)
        # self.fields['image'].upload_to = f'user_{user_id}/images/'
        # self.fields['thumb'].upload_to = f'user_{user_id}/images/'


    def get_get_visit_title(self, obj):
        title = getattr(obj.visit, 'title', None)
        return title
       

    def get_get_visit_url(self, obj):
        request=self.context.get('request', {})
        visit = getattr(obj, 'visit', None)
        if not visit:
            return None
        return reverse('api:visit-detail', kwargs={'pk': visit.pk}, request=request)

        
    def get_get_visit_image_url(self, obj):
        return reverse_url(self,obj,name='image')
        
    

    def get_get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request',{})
            if request:
                return request.build_absolute_uri(obj.image_url)
            return obj.image_url
        return None

        
    def get_get_thumb_url(self, obj):
        if obj.thumb:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.thumb_url)
            return obj.thumb_url
        return None


    def create(self, validated_data):
        request_user = self.context['request'].user
        visitimagefile = VisitImageFile(**validated_data)
        visitimagefile.user = request_user
        visitimagefile.save()
        return visitimagefile
    
    
class UploadedImagesNestedSerializer(MappingModelSerializer):
    
    get_image_url=serializers.SerializerMethodField()
    get_thumb_url=serializers.SerializerMethodField()

    mapping = {  
        'get_image_url':'Image Link',
        'get_thumb_url':'Thumbnail Link',      
    } 
    class Meta:
        model = VisitImageFile
        fields = ['get_image_url', 'get_thumb_url']

    def get_get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request', None)
            if request:
                return request.build_absolute_uri(obj.image_url)
            return obj.image_url
        return None

    def get_get_thumb_url(self, obj):
        if obj.thumb:
            request = self.context.get('request', None)
            if request:
                return request.build_absolute_uri(obj.thumb_url)
            return obj.thumb_url
        return None

