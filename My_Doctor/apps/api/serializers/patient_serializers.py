from apps.core.models import Patient, User
from rest_framework import serializers
# from apps.api.serializers import UserPublicSerializer, UserUpdateSerializer, UserPrivateSerializer  
from apps.api.serializers import user_serializers


class PatientPublicSerializer(serializers.ModelSerializer):
    """
    Serializer for Patient's public view
    """
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    user = user_serializers.UserPublicSerializer(read_only=True)
    
    class Meta:
        model = Patient
        fields = ['user','tracks']
        
       

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
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    user = user_serializers.UserVisitSerializer
    
    class Meta:
        model = Patient
        # fields = '__all__'
        fields = ['user','adress','birth_date','tracks']



class PatientUpdateSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    user = user_serializers.UserUpdateSerializer()
    
    class Meta:
        model = Patient
        fields = ['tracks','adress', 'birth_date','phone', 'user']
        # fields = '__all__'







