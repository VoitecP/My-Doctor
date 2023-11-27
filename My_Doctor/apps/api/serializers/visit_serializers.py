from apps.core.models import Visit, VisitImageFile, User, Patient, Doctor
from rest_framework import serializers
from .doctor_serializers import DoctorPublicSerializer, DoctorPrivateSerializer, DoctorVisitSerializer
from .patient_serializers import *
from .category_serializers import *
#PatientPublicSerializer, PatientPrivateSerializer, PatientVisitSerializer
from .file_serializers import VisitImageSerializer
from rest_framework.reverse import reverse



#####
#####

class VisitListPTypeSerializer(serializers.ModelSerializer):

    doctor_visit=DoctorVisitSerializer(label='doctor', source='doctor', read_only=True)
    visit_status=serializers.SerializerMethodField(label='visit status', source ='closed', read_only=True)
    visit_category=CategoryPublicSerializer(label='category', source='category', read_only=True)
    visit_price=serializers.SerializerMethodField(label='url',read_only=True)
    url=serializers.SerializerMethodField(label='url',read_only=True)
    class Meta:
        model = Visit
        fields = ['id', 
                  'url',
                'title',
                #'patient', 
                'doctor_visit',       
                'category',
                'visit_category',
                #'image',
                #'images',
                #'description',
                'price',
                'visit_status']
        extra_kwargs =  {'doctor': {'write_only': True},
                        'category': {'write_only': True},
                        'closed': {'write_only': True}}
        
    
    def get_visit_status(self, obj):
        if obj.closed == True:
            return  'Visit Closed'
        if obj.closed == False:
            return 'Visit Open'   

    def get_url(self,obj):
        request=self.context.get('request')

        if request is None:
            return None
        return reverse('api:visit-detail', kwargs={"pk": obj.pk}, request=request)
        #return 'reverse'
class VisitRetrievePTypeSerializer(serializers.ModelSerializer):
    
    doctor_visit=DoctorVisitSerializer(label='doctor', source='doctor', read_only=True)
    visit_status=serializers.SerializerMethodField(label='visit status', source ='closed', read_only=True)
    #url=serializers.SerializerMethodField(label='url')
    class Meta:
        model = Visit
        fields = ['id', 
                  'url',
                'title',
                #'patient', 
                'doctor',
                'doctor_visit',       
                'category',
                'image',
                'images',
                'description',
                'price',
                'visit_status']
        extra_kwargs =  {'doctor': {'write_only': True},
                        'category': {'write_only': True},
                        'closed': {'write_only': True}}
        
    def get_visit_status(self, obj):
        if obj.closed == True:
            return  'Visit Closed'
        if obj.closed == False:
            return 'Visit Open'
        
    # def get_url(self,obj):
    #     request=self.context.get('request')

    #     if request is None:
    #         return None
    #     return reverse('api:visit-detail', kwargs={"pk": obj.pk}, request=request)
        
    
    
        

    pass

class VisitUpdatePTypeSerializer(serializers.ModelSerializer):
    
    doctor_visit=DoctorVisitSerializer(label='doctor', source='doctor', read_only=True)
    visit_status=serializers.SerializerMethodField(label='visit status', source ='closed', read_only=True)
    #url=serializers.SerializerMethodField(label='url')
    class Meta:
        model = Visit
        fields = ['id', 
                  'url',
                'title',
                #'patient', 
                #'doctor',
                'doctor_visit',       
                'category',
                'image',
                'images',
                'description',
                #'price',
                'visit_status']
         
        extra_kwargs =  {'category': {'write_only': True},
                        'closed': {'write_only': True}}
        
    def get_visit_status(self, obj):
        if obj.closed == True:
            return  'Visit Closed'
        if obj.closed == False:
            return 'Visit Open'

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