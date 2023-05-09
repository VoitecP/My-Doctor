from apps.core.models import Patient, User
from rest_framework import serializers
from apps.api.serializers import UserPublicSerializer  

class PatientSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Patient
        fields = '__all__'


##

class PatientPrivateSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Patient
        fields = '__all__'



class PatientPublicSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    user = UserPublicSerializer(read_only=True)
    
    class Meta:
        model = Patient
        #fields = ['user.person.first_name','user.person.last_name','tracks']
        # fields = ['tracks','public_user','birth_date']
        fields = '__all__'
        #  nested serializer 
       

class PatientVisitSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Patient
        fields = '__all__'