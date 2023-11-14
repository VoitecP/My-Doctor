from apps.core.models import Patient, User
from rest_framework import serializers
from rest_framework.reverse import reverse
# from apps.api.serializers import UserPublicSerializer, UserUpdateSerializer, UserPrivateSerializer  
from apps.api.serializers import user_serializers


class PatientPublicSerializer(serializers.ModelSerializer):
    """
    Serializer for Patient's public view
    """
    #tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
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


class PatientVisitSerializer(serializers.ModelSerializer):
    """
    Only connected thru common visit can see these fields
    """
    #patient = user_serializers.UserVisitSerializer
    # first name,  last name,  email
    url=serializers.SerializerMethodField(read_only=True)
    first_name=serializers.SerializerMethodField(label='first name', read_only=True)
    last_name=serializers.SerializerMethodField(label='last name', read_only=True)
    email=serializers.SerializerMethodField(read_only=True)

    
    class Meta:
        model = Patient
        # fields = '__all__'
        fields = ['url','first_name','last_name','email',
                  'birth_date']

    def get_url(self,obj):
        request=self.context.get('request')
       
        if request is None:
            return None
        #return reverse('viewsets-patients', kwargs={"pk": obj.pk}, request=request)
        return 'reverse'
    
    def get_first_name(self, obj):
        return obj.user.first_name
    
    def get_last_name(self, obj):
        return obj.user.last_name
    
    def get_email(self, obj):
        return obj.user.email



class PatientUpdateSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    user = user_serializers.UserUpdateSerializer()
    
    class Meta:
        model = Patient
        fields = ['tracks','adress', 'birth_date','phone', 'user']
        # fields = '__all__'







