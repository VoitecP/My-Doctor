from rest_framework import serializers
from rest_framework.reverse import reverse

from apps.core.models import Doctor, Patient,  Visit, VisitImageFile
from .doctor_serializers import DoctorPublicSerializer, DoctorPrivateSerializer, DoctorVisitSerializer
from .patient_serializers import *  # todo remove when removing junk serializers
from .category_serializers import *
from .file_serializers import VisitImageSerializer, UploadedImagesNestedSerializer
from .serializer_mixins import MappingModelSerializer, DynamicModelSerializer


class VisitDynamicSerializer(DynamicModelSerializer):

    ## Fields for 'List'
    get_title = serializers.CharField(label='Title', source='title', read_only=True)
    get_url = serializers.SerializerMethodField()
    get_category = serializers.CharField(label='Category', source='category', read_only = True)
    get_patient =  serializers.CharField(label='Patient',  source='patient.full_name', read_only=True)
    get_doctor =  serializers.CharField(label='Doctor',  source='doctor.full_name', read_only=True)
    # Fields for 'Retrieve'
    get_date = serializers.DateTimeField(label='Visit Date',  format='%d-%m-%Y %H:%M:%S', source='date', read_only=True)
    get_url_patient = serializers.SerializerMethodField()
    get_url_doctor = serializers.SerializerMethodField()
    get_description = serializers.CharField(label='Description', source='description', read_only=True)
    get_uploaded_images = UploadedImagesNestedSerializer(label='Uploaded Images', source='visit_images', many=True, read_only=True)
    get_price = serializers.CharField(label='Price', source='price', read_only=True)
    # get_closed = serializers.BooleanField(label='Visit Closed', source='closed', read_only=True)
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
        'get_title':'title',
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


    def get_dynamic_fields(self, instance, action, request_user):
        fields = []

        if action == 'list':
            if request_user.usertype == 'p': 

                fields = ['get_title','get_url','get_category',
                          'get_doctor']

            elif request_user.usertype == 'd':

                fields = ['get_title','get_url','get_category',
                          'get_patient']
    
            elif (request_user.usertype == 'c' 
                  or request_user.is_staff == True):
                
                fields = ['get_title','get_url','get_category',
                          'get_patient','get_doctor']
                
            else:
                fields = []

        if action == 'create':
            if request_user.usertype == 'p':
                
                fields = ['title','category','date', 
                          'doctor', 
                          'uploaded_images',
                          'description']
            
            elif request_user.usertype == 'd':
                fields = []

            elif (request_user.usertype == 'c' 
                  or request_user.is_staff == True):
               
                fields = ['title','category','date', 
                          'patient','doctor', 
                          'uploaded_images',
                          'description','price','closed']
            
            else:
                fields = []

        if action in ['retrieve','destroy']:
            if request_user.usertype == 'p': 
            
                fields = ['get_title','get_category','get_date',
                          'get_doctor','get_url_doctor','get_description',
                          'get_uploaded_images',
                          'get_price','get_closed']

            elif request_user.usertype == 'd':

                fields = ['get_title','get_category','get_date',
                          'get_patient','get_url_patient','get_description',
                          'get_uploaded_images',
                          'get_price','get_closed']

            elif (request_user.usertype == 'c' 
                  or request_user.is_staff == True):
                
                fields = ['get_title','get_category','get_date',
                          'get_patient','get_url_patient', 'get_doctor',
                          'get_url_doctor','get_description',
                          'get_uploaded_images','get_price',
                          'get_closed']

            else:
                fields - []

        if action in ['update','partial_update']:
            if request_user.usertype == 'p': 
        
                fields = ['title','category','date',  
                          'uploaded_images',
                          'description']
            
            elif request_user.usertype == 'd':

                fields = ['title','category','date',  
                          'uploaded_images',
                          'description','price','closed']

            elif (request_user.usertype == 'c' 
                  or request_user.is_staff == True):
                
                fields = ['title','category','date', 
                          'patient','doctor', 
                          'uploaded_images',
                          'description','price','closed']

            else:
                fields = []
    
        return fields
        

    def get_get_url(self, obj):
        request=self.context.get('request')
        if request is None:
            return None
        return reverse('api:visit-detail', kwargs={'pk': obj.pk}, request=request)
    

    def get_get_url_patient(self, obj):
        request=self.context.get('request')
        if not request:
            return None
        return reverse('api:patient-detail', kwargs={'pk': obj.patient.pk}, request=request)
       

    def get_get_url_doctor(self, obj):
        request=self.context.get('request')
        if not request :
            return None
        return reverse('api:doctor-detail', kwargs={'pk': obj.doctor.pk}, request=request)
       

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


#####
# Visit Serializers for Patient
#####

class VisitListSerializerForPatient(serializers.ModelSerializer):
    '''
    Serializer for GET/List of instances
    '''

    doctor_visit=DoctorVisitSerializer(label='doctor', source='doctor', read_only=True)
    visit_status=serializers.SerializerMethodField(label='visit status', source ='closed', read_only=True)
    visit_category=serializers.SerializerMethodField(label='Visit Category', read_only=True)
    visit_price=serializers.SerializerMethodField(label='url',source='price',read_only=True)
    url=serializers.SerializerMethodField(label='url',read_only=True)
    class Meta:
        model = Visit
        fields = ['id', 
                  'url',
                'title',
                #'patient', 
                'doctor_visit',       
                #'category',
                'visit_category',
                #'image',
                #'images',
                #'description',
                'visit_price',
                'visit_status']
        # extra_kwargs =  {'doctor': {'write_only': True},
        #                 'category': {'write_only': True},
        #                 'closed': {'write_only': True},
        #                 'price':{'write_only':True}}
        
    
    def get_visit_status(self, obj):
        if obj.closed == True:
            return  'Visit Closed'
        if obj.closed == False:
            return 'Visit Open'   
        
    def get_visit_price(self, obj):
        return  obj.price
    
            
    def get_url(self,obj):
        request=self.context.get('request')

        if request is None:
            return None
        return reverse('api:visit-detail', kwargs={"pk": obj.pk}, request=request)
        #return 'reverse'

    def get_visit_category(self, obj):
        if obj.category.name:
            return obj.category.name
        else: 
            return 'empty'
class VisitRetrieveSerializerForPatient(serializers.ModelSerializer):
    '''
    Serializer for GET/Retrieve instance,  POST/Create instance or DEL/Destroy instance
    '''
    doctor_visit=DoctorVisitSerializer(label='doctor', source='doctor', read_only=True)
    visit_category=CategorySerializer(label='Category', read_only=True)
    visit_status=serializers.SerializerMethodField(label='visit status', source ='closed', read_only=True)
    visit_price=serializers.SerializerMethodField(label='Visit Price', source='price')
    #url=serializers.SerializerMethodField(label='url')
    class Meta:
        model = Visit
        fields = ['id', 
                  #'url',
                'title',
                'patient', 
                'doctor',
                'doctor_visit',  
                'visit_category',     
                'category',
                'image',
                'images',
                'description',
                'visit_price',
                'visit_status']
        extra_kwargs =  {'doctor': {'write_only': True},
                        'category': {'write_only': True},
                        # 'price':{'write_only':True},
                        # 'closed': {'write_only': True}
                        }
        
    def get_visit_status(self, obj):
        if obj.closed == True:
            return  'Visit Closed'
        if obj.closed == False:
            return 'Visit Open'
        
    def get_visit_price(self, obj):
        return  obj.price
    

class VisitUpdateSerializerForPatient(serializers.ModelSerializer):
    '''
    Serializer for PUT/Update instance
    '''
    
    # doctor_visit=DoctorVisitSerializer(label='doctor', source='doctor', read_only=True)
    # visit_status=serializers.SerializerMethodField(label='visit status', source ='closed', read_only=True)
    #url=serializers.SerializerMethodField(label='url')
    class Meta:
        model = Visit
        fields = ['id', 
                #   'url',
                'title',
                #'patient', 
                'doctor',
                # 'doctor_visit',       
                'category',
                'image',
                'images',
                'description',
                #'price',
                # 'visit_status'
                ]
         
        # extra_kwargs =  {'category': {'write_only': True},
        #                 }
        
    # def get_visit_status(self, obj):
    #     if obj.closed == True:
    #         return  'Visit Closed'
    #     if obj.closed == False:
    #         return 'Visit Open'

#####
# Visit Serializers for Doctor
#####

class VisitListSerializerForDoctor(serializers.ModelSerializer):
    '''
    Serializer for GET/List of instances
    '''

    patient_visit = serializers.SerializerMethodField(label='patient visit',read_only=True)
    visit_status=serializers.SerializerMethodField(label='visit status', source ='closed', read_only=True)
   
    visit_category=serializers.SerializerMethodField(label='visit category', read_only=True)
    visit_price=serializers.SerializerMethodField(label='url',source='price',read_only=True)
    url=serializers.SerializerMethodField(label='url',read_only=True)
    class Meta:
        model = Visit
        fields = [ 
                'url',
                'title',
                'patient_visit', 
                #'doctor_visit',       
                #'category',
                'visit_category',
                #'image',
                #'images',
                #'description',
                'visit_price',
                'visit_status']
        
        # extra_kwargs =  {'doctor': {'write_only': True},
        #                 'category': {'write_only': True},
        #                 'closed': {'write_only': True},
        #                 'price':{'write_only':True}}
        
    
    def get_visit_status(self, obj):
        if obj.closed == True:
            return  'Visit Closed'
        if obj.closed == False:
            return 'Visit Open'   
        
    def get_visit_price(self, obj):
        return  obj.price
    
            
    def get_url(self, obj):
        request=self.context.get('request')

        if request is None:
            return None
        return reverse('api:visit-detail', kwargs={"pk": obj.pk}, request=request)
        #return 'reverse'

    def get_visit_category(self, obj):
        return obj.category.name
        
    def get_patient_visit(self, obj):
        return obj.patient.full_name

class VisitRetrieveSerializerForDoctor(serializers.ModelSerializer):
    '''
    Serializer  GET/Retrieve instance, POST/Create instance and DEL/Destroy Instance
    '''
    
    #doctor_visit=DoctorVisitSerializer(label='doctor', source='doctor', read_only=True)
    # TODO Fix patient/user serialzier and models to not put empty fields
    patient_visit=PatientDocotorVisitSerializer(label='Patient Visit', read_only=True)
    visit_status=serializers.SerializerMethodField(label='visit status', read_only=True)
    visit_category=CategorySerializer(label='category', source='category', read_only=True)
    visit_price=serializers.SerializerMethodField(label='Visit Price', read_only=True)
    #url=serializers.SerializerMethodField(label='url')
    class Meta:
        model = Visit
        fields = [
                'id', 
                'title',
                'patient',
                'patient_visit', 
                #'doctor',
                # 'doctor_visit',
                'visit_category',       
                # 'category',
                'image',  # TODO Set proper field for images.
                'images',
                'description',
                'visit_price',
                'price',
                'visit_status',
                
                ]
        # extra_kwargs =  {
        #                 # 'category': {'write_only': True},
        #                 # 'price':{'write_only':True},
        #                 }
        
    def get_visit_status(self, obj):
        if obj.closed == True:
            return  'Visit Closed'
        if obj.closed == False:
            return 'Visit Open'
        
    def get_visit_price(self, obj):
        return  obj.price
    
class VisitUpdateSerializerForDoctor(serializers.ModelSerializer):
    '''
    Serializer for  PUT/Update instance,
    '''

    # doctor_visit=DoctorVisitSerializer(label='doctor', source='doctor', read_only=True)
    # visit_status=serializers.SerializerMethodField(label='visit status', read_only=True)
    closed=serializers.BooleanField(label='Is visit closed')

    class Meta:
        model = Visit
        fields = [ 
                'id',
                #'title',
                #'patient', 
                #'doctor',
                
                ## Not need it is only update serializer
                #'doctor_visit',       
                'category',
                'image',
                'images',
                'description',
                'price',
                'closed',
                #'visit_status'
                ]
         
        extra_kwargs =  {'category': {'write_only': True},
                        'price':{'write_only':True},
                        'closed': {'write_only': True}}
          

#####
# Visit Serializers for Director
#####

class VisitListSerializerForDirector(serializers.ModelSerializer):
    '''
    Serializer for GET/List of instances
    '''
    patient_visit=serializers.SerializerMethodField(label='patient', read_only=True)
    doctor_visit=serializers.SerializerMethodField(label='doctor visit', read_only=True)
    visit_status=serializers.SerializerMethodField(label='visit status', read_only=True)
    visit_category=serializers.SerializerMethodField(label='category', source='category', read_only=True)
    visit_price=serializers.SerializerMethodField(label='url',source='price',read_only=True)
    url=serializers.SerializerMethodField(label='url',read_only=True)
    class Meta:
        model = Visit
        fields = ['id', 
                  'url',
                'title',
                #'patient', 
                'patient_visit',
                'doctor_visit',       
                #'category',
                'visit_category',
                #'image',
                #'images',
                #'description',
                'visit_price',
                'visit_status']
        # extra_kwargs =  {'doctor': {'write_only': True},
        #                 'category': {'write_only': True},
        #                 'closed': {'write_only': True},
        #                 'price':{'write_only':True}}
        
    def get_patient_visit(self, obj):
        return obj.patient.full_name  

    def get_doctor_visit(self, obj):
        return obj.doctor.full_name    
    
    def get_visit_status(self, obj):
        if obj.closed == True:
            return  'Visit Closed'
        if obj.closed == False:
            return 'Visit Open'   
        
    def get_visit_price(self, obj):
        return  obj.price
    
            
    # def get_visit_category(self, obj):
    #     return obj.category.name  
    def get_visit_category(self, obj):
        try:
            return obj.category.name
        except: 
            return 'empty'
          
    def get_url(self,obj):
        request=self.context.get('request')

        if request is None:
            return None
        return reverse('api:visit-detail', kwargs={"pk": obj.pk}, request=request)
        #return 'reverse'


class VisitRetrieveSerializerForDirector(serializers.ModelSerializer):
    '''
    Serializer for GET/Retrieve instance,  POST/Create instance or DEL/Destroy instance
    '''
    patient_visit=PatientDocotorVisitSerializer(label='Patient Visit', read_only=True)
    doctor_visit=DoctorVisitSerializer(label='doctor', source='doctor', read_only=True)
    visit_status=serializers.SerializerMethodField(label='visit status', source ='closed', read_only=True)
    category_visit=serializers.SerializerMethodField(label='Categor Visit', read_only=True)
    visit_price=serializers.SerializerMethodField(label='Visit Price', source='price')
    #url=serializers.SerializerMethodField(label='url')
    class Meta:
        model = Visit
        fields = ['id', 
                'title',
                'patient',
                'patient_visit',
                'doctor',
                'doctor_visit',       
                'category',
                'category_visit',
                'image',
                'images',
                'description',
                'price',
                'visit_price',
                'closed',
                'visit_status']
        extra_kwargs =  {
                        'patient':{'write_only':True},
                        'doctor': {'write_only': True},
                        'category': {'write_only': True},
                        'price':{'write_only':True},
                        'closed': {'write_only': True}}
        
    def get_visit_status(self, obj):
        if obj.closed == True:
            return  'Visit Closed'
        if obj.closed == False:
            return 'Visit Open'
        
    def get_visit_price(self, obj):
        return  obj.price
    
    def get_category_visit(self, obj):
        return obj.category.name


class VisitUpdateSerializerForDirector(serializers.ModelSerializer):
    '''
    Serializer for  PUT/Update instance,
    '''
    
    # doctor_visit=DoctorVisitSerializer(label='doctor', source='doctor', read_only=True)
    # visit_status=serializers.SerializerMethodField(label='visit status', source ='closed', read_only=True)
    #url=serializers.SerializerMethodField(label='url')
    closed=serializers.BooleanField(label='Is visit closed')
    class Meta:
        model = Visit
        fields = ['id', 
                #   'url',
                'title',
                'patient', 
                'doctor',
                #'doctor_visit',       
                'category',
                'image',
                'images',
                'description',
                'price',
                'closed',
                ]
         
        extra_kwargs =  {
                        'patient': {'write_only': True},
                        'docotor': {'write_only': True},
                        'category': {'write_only': True},
                        'closed': {'write_only': True}}
        
    def get_visit_status(self, obj):
        if obj.closed == True:
            return  'Visit Closed'
        if obj.closed == False:
            return 'Visit Open'





##########
## Other serializers

#####
#####
class VisitPublicSerializer(serializers.ModelSerializer):
    """
    Director can see, all visits
    """
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    doctor = DoctorPublicSerializer(read_only=True)
    patient = PatientPublicSerializer(read_only=True)

    class Meta:
        model = Visit
        # fields = '__all__'      # only price, patient and doctor fields
        fields =['id','tracks','patient','doctor','price']

# Public serializer for category , doctor, patient
# TODO  ## user.doctor can see all public patients

class VisitRetrieveViewsetSerializer(serializers.ModelSerializer):

    patient_visit=PatientForPatientSerializer(label='patient', source='patient', read_only=True)
    doctor_visit=DoctorVisitSerializer(label='doctor', source='doctor', read_only=True)
    
   
    class Meta:
        model = Visit
        fields=['id', 'title',
                'patient',
                'patient_visit',  
                'doctor',
                'doctor_visit',       
                'category','image','images','description','price']
  
        extra_kwargs = {'patient': {'write_only': True},
                        'doctor': {'write_only': True},
                        'category': {'write_only': True}
                        }
        # exclude=['patient']

# }



class VisitViewsetSerializer(serializers.ModelSerializer):



    
    #patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(),write_only=True)
    #TODO patient specific serializers
    #patient_visit=PatientForPatientSerializer(label='patient', source='patient', read_only=True)

    patient_visit=PatientUpdateSerializer(label='patient', source='patient', read_only=True)
    #doctor = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all(),write_only=True)
    doctor_visit=DoctorVisitSerializer(label='doctor', source='doctor', read_only=True)
    #category_public=
    #images = VisitImageSerializer(many=True, read_only=True)
    price_visit=serializers.SerializerMethodField()
    

    def get_price_visit(self, obj):
        if obj.closed==True:
            return f'closed {obj.price}'
        else:
            return f'open {obj.price}'
   
    class Meta:
        model = Visit
        fields = ['id', 'title',
                'patient',
                'patient_visit',  
                'doctor',
                'doctor_visit',       
                'category','image','images','description','price',
                'price_visit',
                ]
  

        extra_kwargs =  {'patient': {'write_only': True},
                        'doctor': {'write_only': True},
                        'category': {'write_only': True}
                        }
       
      
    
# TODO base serializer for Visits
class VisitPrivateSerializer(serializers.ModelSerializer):
    """
    Patient and doctor can see related visit
    """
    images = VisitImageSerializer(many=True, read_only=True)
    visit_doctor = DoctorPrivateSerializer(source='doctor',read_only=True)  # Disable to allow choose doctor
    patient = PatientForPatientSerializer(read_only=True)

    uploaded_images = serializers.ListField(
        child = serializers.ImageField(max_length = 1000000, allow_empty_file = False, use_url = False),
        write_only=True)

    class Meta:
        model = Visit
        # fields = '__all__'
        fields = ['id','patient', 'doctor','price', 'visit_doctor',
                  'images','description','category', 'uploaded_images']


    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        visit = Visit.objects.create(**validated_data)
        for image in uploaded_images:
            VisitImageFile.objects.create(visit=visit, image=image)
        return visit
    
    

##

class VisitUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for Update Visit Model
    """
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    doctor = DoctorPublicSerializer(read_only=True)
    patient = PatientPublicSerializer(read_only=True)

    class Meta:
        model = Visit
        fields = '__all__'


class VisitDeleteSerializer(serializers.ModelSerializer):
    """
    Serializer for delete Visit mMdel
    """
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    doctor = DoctorPublicSerializer(read_only=True)
    patient = PatientPublicSerializer(read_only=True)

    class Meta:
        model = Visit
        fields = '__all__'
        

class VisitCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for delete Visit mMdel
    """
    images = VisitImageSerializer(many=True, read_only=False)
    doctor = DoctorPublicSerializer(read_only=True)
    patient = PatientPublicSerializer(read_only=True)
   

    class Meta:
        model = Visit
        # fields = '__all__'
        fields = ['title','date','category','description', 'images','price','patient','doctor']

   

    def perform_create(self, validated_data):
        visit = Visit.objects.create(
            # TODO  replace  create(**validated_data)
            validated_data['title'], 
            validated_data['date'], 
            validated_data['patient'],
            validated_data['doctor'],
            validated_data['category'],
            validated_data['images'],
            validated_data['description'],
            validated_data['price'])
        visit.title = validated_data['title']
        visit.date = validated_data['date']
        visit.patient = validated_data['patient']
        visit.doctor = validated_data['doctor']
        visit.category = validated_data['category']
        visit.images = validated_data['images']
        visit.description = validated_data['decsription']
        visit.price = validated_data['price']
        visit.save()
        return visit  


    #     class RatingViewSet(ModelViewSet):
    # # queryset = Rating.objects.all()
    # serializer_class = RatingSerializer
    # permission_classes = [IsAuthenticated]
    
    # def get_queryset(self):
    #     return Rating.objects.filter(product_id = self.kwargs['product_pk'])
    
    # def get_serializer_context(self):
    #     user_id = self.request.user.id
    #     product_id = self.kwargs["product_pk"]
    #     return {"user_id": user_id, "product_id": product_id}


    
# class AlbumSerializer(serializers.ModelSerializer):
#     tracks = TrackListingField(many=True)

#     class Meta:
#         model = Album
#         fields = ['album_name', 'artist', 'tracks']