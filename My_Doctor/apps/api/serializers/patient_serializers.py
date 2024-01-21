from django.db.models import Sum
from rest_framework import serializers
from rest_framework.reverse import reverse

from apps.api.serializers import user_serializers
from apps.core.models import Patient, Visit
from .serializer_mixins import  DynamicModelSerializer, reverse_url


class PatientDynamicSerializer(DynamicModelSerializer):

    ## Fields for 'List' , 'create'
    get_full_name=serializers.CharField(label='Full Name', source='full_name', read_only=True)
    get_url=serializers.SerializerMethodField()

    ## Fields for 'retrieve' , 'destroy', 
    get_first_name=serializers.CharField(label='First Name', source='user.first_name', read_only=True)
    get_last_name=serializers.CharField(label='Last Name', source='user.last_name', read_only=True)
    get_birth_date = serializers.DateField(label='Birth Date', source='birth_date', read_only=True)
    # Visit related fields
    get_email=serializers.CharField(label='Email', source='user.email', read_only=True)
    # Private fields
    get_adress = serializers.CharField(label='Adress', source='adress', read_only=True)
      
    ## Fields for 'update' , 'partial_update'
    first_name=serializers.CharField(source='user.first_name', max_length=150, default='', allow_blank=True)
    last_name=serializers.CharField(source='user.last_name',  max_length=150, default='', allow_blank=True)
    birth_date=serializers.DateField(default='')
    email=serializers.CharField(source='user.email', max_length=100, default='', allow_blank=True)
    adress=serializers.CharField(max_length=100, default='', allow_blank=True)
    
    mapping={
        'get_full_name':'Full Name',
        'get_url':'Link',
        #
        'get_first_name':'First Name',
        'get_last_name':'Last Name',
        'get_email':'Email',
        'get_birth_date':'Birth Date',
        'get_adress':'Adress',     
    }

    class Meta:
        model = Patient
        fields = '__all__'


    def get_dynamic_fields(self, instance, custom_action, request_user):
        fields = set()
        owner = bool(instance and instance.user == request_user)
        retrieve_fields = {'get_first_name','get_last_name',
                          'get_birth_date','get_email', 
                          'get_adress'}
        update_fields = {'first_name','last_name',
                         'birth_date','email',
                         'adress'}
        
        if custom_action in ['list','create']:
            fields = {'get_full_name','get_url'}
    
        if custom_action in ['retrieve','destroy']:
            if owner:
                fields = retrieve_fields
            else:
                fields = retrieve_fields - {'get_email','get_adress'}

        if custom_action in ['update','partial_update']:
            if owner:
                fields = update_fields
        return fields
        

    def get_get_url(self, obj):
        return reverse_url(self, obj)


## Junk serializers
class PatientPublicSerializer(serializers.ModelSerializer):
    """
    Serializer for Patient's public view
    """
    #tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    user = user_serializers.UserPublicSerializer(read_only=True)
    
    class Meta:
        model = Patient
        fields = ['user']
        
class PatientDocotorVisitSerializer(serializers.ModelSerializer):
# tODO  Make serializer with common visits with doctor.
    user = user_serializers.UserPublicSerializer(read_only=True)
    class Meta:
        model = Patient
        fields = ['user']
       

class PatientPrivateSerializer(serializers.ModelSerializer):
    """
    Only logged user can view these fields , self fields.
    """
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    user = user_serializers.UserPrivateSerializer(read_only=True)
    
    class Meta:
        model = Patient
        fields = ['user','adress','birth_date','tracks']


class PatientForDoctorSerializer(serializers.ModelSerializer):
    """
    Only doctors connected thru common visit can see these Patients
    """
    #patient = user_serializers.UserVisitSerializer
    # first name,  last name,  email
    url=serializers.SerializerMethodField(read_only=True)
    first_name=serializers.SerializerMethodField(label='first name', read_only=True)
    last_name=serializers.SerializerMethodField(label='last name', read_only=True)
    email=serializers.SerializerMethodField(read_only=True)
    visits=serializers.SerializerMethodField(read_only=True)
    total_prices=serializers.SerializerMethodField(label='Total prices',read_only=True)
    
    class Meta:
        model = Patient
        # fields = '__all__'
        fields = ['url','first_name','last_name','email',
                  'birth_date','visits','total_prices']

    def get_url(self,obj):
        request=self.context.get('request')
       
        if request is None:
            return None
        return reverse('api:patient-detail', kwargs={"pk": obj.pk}, request=request)
        #return 'reverse'
    
    def get_first_name(self, obj):
        return obj.user.first_name
    
    def get_last_name(self, obj):
        return obj.user.last_name
    
    def get_email(self, obj):
        return obj.user.email
    
    def get_visits(self, obj):
        return Visit.objects.filter(patient=obj).count()
    
    def get_total_prices(self, obj):
        total=Visit.objects.filter(patient=obj).aggregate(sum=Sum('price'))
        return total['sum']
        # return Visit.objects.filter(patient=obj).aggregate(sum=Sum('price'))

class PatientForPatientSerializer(serializers.ModelSerializer):

    pass

class PatientUpdateSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    user = user_serializers.UserUpdateSerializer()
    
    class Meta:
        model = Patient
        fields = ['tracks','adress', 'birth_date','phone', 'user']
        # fields = '__all__'







