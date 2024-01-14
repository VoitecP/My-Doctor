from apps.core.models import VisitImageFile, ImageFile, Visit
from rest_framework import serializers
# from apps.api.serializers import UserPublicSerializer, UserPrivateSerializer, UserVisitSerializer

from rest_framework.reverse import reverse

from rest_framework.response import Response 
from rest_framework.serializers import ValidationError
from apps.api.serializers.serializer_mixins import MappingMixin


class MixinModelSerializer(MappingMixin, serializers.ModelSerializer):    
    pass

class VisitImageDynamicSerializer(MixinModelSerializer):

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
        

    def __init__(self, *args, **kwargs):
        context = kwargs.get('context', {})
        action = context.get('action')
        request_user = context['request'].user
        self.fields['visit'].queryset = Visit.objects.filter(patient_id=request_user.id)
        
        self.fields['image'].upload_to = f'user_{request_user.id}/images/'
        self.fields['thumb'].upload_to = f'user_{request_user.id}/images/'

        if action in ['list']:
            # if request_user.usertype == 'p': 
            fields = ['get_visit_title','get_visit_image_url']

        if action in ['create']:
            fields = ['image','visit']

        if action in ['retrieve','destroy']:
            fields = ['get_visit_title', 'get_visit_url',
                      'get_image_url','get_thumb_url']
        
        if action in ['update','partial_update']:
            fields = []

        super().__init__(*args, **kwargs)
        dynamic = set(fields)
        all_fields = set(self.fields)

        for field_pop in all_fields - dynamic:
            self.fields.pop(field_pop)


    def get_get_visit_title(self, obj):
        title = getattr(obj.visit, 'title', None)

        if title is not None:
            return obj.visit.title
        else: 
            return 'None'


    def get_get_visit_url(self, obj):
        request=self.context.get('request')
        visit = getattr(obj, 'visit', None)

        if visit is None:
            return 'None'
        return reverse('api:visit-detail', kwargs={'pk': visit.pk}, request=request)

        
    def get_get_visit_image_url(self, obj):
        request=self.context.get('request')

        if request is None:
            return None
        return reverse('api:image-detail', kwargs={'pk': obj.pk}, request=request)
    

    def get_get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image_url)
            else:
                return obj.image_url
        else:
            return 'None'

        
    def get_get_thumb_url(self, obj):
        if obj.thumb:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.thumb_url)
            else:
                return obj.thumb_url
        else:
            return 'None'


    def create(self, validated_data):
    
        request_user = self.context['request'].user
        visitimagefile = VisitImageFile(**validated_data)
        visitimagefile.user = request_user
        visitimagefile.save()

        return visitimagefile
    
    
class UploadedImagesNestedSerializer(MixinModelSerializer):
    
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
            else:
                return obj.image_url
        else:
            return 'None'

    def get_get_thumb_url(self, obj):
        if obj.thumb:
            request = self.context.get('request', None)
            if request:
                return request.build_absolute_uri(obj.thumb_url)
            else:
                return obj.thumb_url
        else:
            return 'None'


###########

# class ProductImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProImage
#         fields = ["id", "product", "image"]


# class ProductSerializer(serializers.ModelSerializer):
#     images = ProductImageSerializer(many=True, read_only=True)
#     uploaded_images = serializers.ListField(
#         child = serializers.ImageField(max_length = 1000000, allow_empty_file = False, use_url = False),
#         write_only=True)
    
#     class Meta:
#         model = Product
#         fields = [ "id", "name", "description", "inventory", "price", "images", "uploaded_images"]
    
    
#     def create(self, validated_data):
#         uploaded_images = validated_data.pop("uploaded_images")
#         product = Product.objects.create(**validated_data)
#         for image in uploaded_images:
#             newproduct_image = ProImage.objects.create(product=product, image=image)
#         return product

###########
class MultipleImageSerializer(serializers.Serializer):
    image_url=serializers.SerializerMethodField()
    thumb_url=serializers.SerializerMethodField()
    #image_link=serializers.CharField(source='image_url')
    images = serializers.ListField(
        child=serializers.ImageField(), 
        required = False
    )

    class Meta:
        model = VisitImageFile  
        fields = '__all__'
        #fields = ['id','title','image_url','thumb_url','image_url2']
        # extra_kwargs = {
        #     'files': {'write_only': True},
        # }

    def __init__(self, *args, **kwargs):
        context = kwargs.get('context', {})
        self.request = context.get('request', None)
        
        super(MultipleImageSerializer, self).__init__(*args, **kwargs)

    def get_image_url(self, obj):
        if self.request:
            return self.request.build_absolute_uri(obj.image_url)
        else:
            return obj.image_url
        
    def get_thumb_url(self, obj):
        if obj.thumb:
            if self.request:
                return self.request.build_absolute_uri(obj.thumb_url)
            else:
                return obj.thumb_url
        else:
            return 'none'
    # def get_image_url(self, obj):
    #     return  obj.image_url

    # def create(self, validated_data):
    #     images = validated_data.pop("images")
    #     try:
    #         visit_image = VisitImageFile.objects.create(
    #         validated_data['image'])
    #         image.user = self.request.user
    #         image.image = validated_data['image']
    #         image.save()
    #         return image
    #     except:
    #         raise ValidationError({"detail": "Operation not allowed"})
        


        uploaded_images = validated_data.pop("uploaded_images")
#         product = Product.objects.create(**validated_data)
#         for image in uploaded_images:
#             newproduct_image = ProImage.objects.create(product=product, image=image)
#         return product



class VisitImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitImageFile
        fields = ['id','title','image_url','thumb_url']



class PatientImageSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = VisitImageFile
        # fields = ['image']
        fields = '__all__'

        


class PatientImageCreateSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = VisitImageFile
        fields = ['image','tracks']
        # fields = '__all__'

    def perform_create(self, validated_data):
        try:
            image = VisitImageFile.objects.create(
            validated_data['image'])
            image.user = self.request.user
            image.image = validated_data['image']
            image.save()
            return image
        except:
            raise ValidationError({"detail": "Operation not allowed"})
        

class PatientImageDeleteSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = VisitImageFile
        # ields = ['image','tracks']
        fields = '__all__'

    