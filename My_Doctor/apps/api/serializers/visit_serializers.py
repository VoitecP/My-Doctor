from rest_framework import serializers

from .file_serializers import  UploadedImagesNestedSerializer
from .serializer_mixins import DynamicModelSerializer, reverse_url
from apps.core.models import (Category, Doctor, Patient,  
                              Visit, VisitImageFile)


class VisitDynamicSerializer(DynamicModelSerializer):
    ## Fields for 'List'
    get_title = serializers.CharField(label='Title', source='title', read_only=True)
    get_url = serializers.SerializerMethodField()
    get_category = serializers.CharField(label='Category', source='category.name', read_only = True)
    get_patient =  serializers.CharField(label='Patient',  source='patient.full_name', read_only=True)
    get_doctor =  serializers.CharField(label='Doctor',  source='doctor.full_name', read_only=True)
    # Fields for 'Retrieve'
    get_date = serializers.DateTimeField(label='Visit Date', format='%d-%m-%Y %H:%M:%S', source='date', read_only=True)
    get_url_patient = serializers.SerializerMethodField()
    get_url_doctor = serializers.SerializerMethodField()
    get_description = serializers.CharField(label='Description', source='description', read_only=True)
    get_uploaded_images = UploadedImagesNestedSerializer(label='Uploaded Images', source='visit_images', many=True, read_only=True)
    get_price = serializers.CharField(label='Price', source='price', read_only=True)
    get_closed = serializers.SerializerMethodField()
    ## Fields for 'Create'
    title = serializers.CharField(max_length=100, label='Title')
    category = serializers.PrimaryKeyRelatedField(label='Category', queryset=Category.objects.all(), allow_null=True, required=False)
    date = serializers.DateTimeField(label='Date', default=None, allow_null=True, required=False)
    patient = serializers.PrimaryKeyRelatedField(label='Patient', queryset=Patient.objects.all(), required=True)
    doctor = serializers.PrimaryKeyRelatedField(label='Doctor', queryset=Doctor.objects.all(), required=True)           
    uploaded_images = serializers.ListField(label='Uploaded Images', child = serializers.ImageField(
            max_length = 100, allow_empty_file = False, use_url = False),
            write_only=True)
    description = serializers.CharField(label='Description', max_length=1000, min_length=10)
    # Fields for 'Update'
    price = serializers.CharField(label='Price', max_length=10)
    closed = serializers.BooleanField(label='Visit Closed', default=False)

    mapping = {  
        'get_title':'Title',
        'get_url':'Link',
        'get_category':'Category',
        'get_date':'Visit Date',
        'get_patient':'Patient Full Name',
        'get_doctor':'Doctor Full Name',
        #
        'get_url_patient':'Patient Link',
        'get_url_doctor':'Doctor Link',
        'get_description':'Description',
        'get_uploaded_images':'Uploaded Images',
        'get_price':'Price',
        'get_closed':'Visit Closed',
    }

    class Meta:
        model = Visit
        fields = '__all__'
        extra_kwargs =  {
                        'title': {'write_only': True},
                        'category': {'write_only': True},
                        'date': {'write_only': True},
                        'patient': {'write_only': True},
                        'doctor': {'write_only': True},
                        'description': {'write_only': True},
                        'price': {'write_only': True},
                        'closed': {'write_only': True}
                        }
    

    def get_dynamic_fields(self, instance, custom_action, request_user):
        fields = set()
        patient = bool(request_user.usertype == 'p')
        doctor  = bool(request_user.usertype == 'd')
        director = bool(request_user.usertype == 'c' or request_user.is_staff)
        list_fields = {'get_title','get_url',
                       'get_category','get_patient',
                       'get_doctor'}
        create_fields = {'title','category',
                        'date', 'patient',
                        'doctor', 'uploaded_images',
                        'description','price',
                        'closed'}
        retrieve_fields = {'get_title','get_category',
                           'get_date','get_patient',
                           'get_url_patient', 'get_doctor',
                           'get_url_doctor','get_description',
                           'get_uploaded_images','get_price',
                           'get_closed'}
        update_fields = {'title','category',
                         'date', 'patient',
                         'doctor','uploaded_images',
                         'description','price',
                         'closed'}

        if custom_action == 'list': 
            if patient: 
                    fields = list_fields - {'get_patient'}
            elif doctor:
                    fields = list_fields - {'get_doctor'}
            elif director:
                    fields = list_fields 
            
        elif custom_action == 'create':
            if patient:
                    fields = create_fields - {'patient', 'price',
                                              'closed'}
            elif doctor:
                    pass
            elif director:            
                    fields = create_fields

        elif custom_action  in ['retrieve','destroy']:
            if patient:
                    fields = retrieve_fields - {'get_patient', 'get_url_patient'}                                           
            elif doctor:
                    fields = retrieve_fields - {'get_doctor', 'get_url_doctor'}
            elif director:
                    fields = retrieve_fields
        
        elif custom_action in ['update','partiral_update'] :
            if patient: 
                    fields = update_fields - {'patient', 'doctor',
                                              'price', 'closed'}
            elif doctor:
                    fields = update_fields - {'patient','doctor'}
            elif director:
                    fields = update_fields
        return fields
                                                              

    def get_get_url(self, obj):
        return reverse_url(self, obj)


    def get_get_url_patient(self, obj):
        return reverse_url(self, obj, name='patient', 
                           kwargs={'pk': obj.patient.pk})


    def get_get_url_doctor(self, obj):
        return reverse_url(self, obj, name='doctor', 
                           kwargs={'pk': obj.doctor.pk})


    def get_get_closed(self, obj):
        if obj.closed:
            return 'Yes'
        return 'No'


    def create(self, validated_data):
        request_user = self.context['request'].user
        uploaded_images = validated_data.pop('uploaded_images', [])

        # visit = Visit.objects.create(**validated_data)
        visit = Visit()
        visit.title = validated_data['title']
        visit.category = validated_data['category']
        visit.date = validated_data['date']
        visit.description = validated_data['description']
        visit.doctor = validated_data['doctor']
        if request_user.usertype == 'p':
            visit.patient = request_user.patient
        else:
            visit.patient = validated_data['patient']    
        visit.save()

        for image in uploaded_images:
            visitimagefile = VisitImageFile()
            visitimagefile.visit = visit
            visitimagefile.image = image
            # visitimagefile.user = request_user
            visitimagefile.save()
        return visit
    

    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        # TOdo Update uploaded images to allow to delete images

        instance.title = validated_data.get('title', instance.title)
        instance.category = validated_data.get('category', instance.category)
        instance.date = validated_data.get('date', instance.date)
        instance.patient = validated_data.get('patient', instance.patient)
        instance.doctor = validated_data.get('doctor', instance.doctor)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.closed = validated_data.get('closed', instance.closed)
        instance.save()

        return instance
