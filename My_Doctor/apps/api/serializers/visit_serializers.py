from apps.core.models import Visit, VisitImageFile, User, Patient, Doctor
from rest_framework import serializers
from .doctor_serializers import DoctorPublicSerializer, DoctorPrivateSerializer, DoctorVisitSerializer
from .patient_serializers import *
from .category_serializers import *
#PatientPublicSerializer, PatientPrivateSerializer, PatientVisitSerializer
from .file_serializers import VisitImageSerializer
from rest_framework.reverse import reverse

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