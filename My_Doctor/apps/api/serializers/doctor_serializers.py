from apps.core.models import Doctor
from rest_framework import serializers
from apps.api.serializers import UserPublicSerializer, UserPrivateSerializer, UserVisitSerializer


class DoctorPublicSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    user = UserPublicSerializer(read_only=True)
    
    class Meta:
        model = Doctor
        fields = ['tracks','user','specialization','phone']
        # fields = '__all__'
         

class DoctorPrivatecSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    user = UserPrivateSerializer(read_only=True)
    
    class Meta:
        model = Doctor
        # fields = ['tracks','user','specialization','phone']
        fields = '__all__'


class DoctoVisitSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    user = UserVisitSerializer(read_only=True)
    
    class Meta:
        model = Doctor
        # fields = ['tracks','user','specialization','phone']
        fields = '__all__'
         


### 

class DoctorSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Doctor
        fields = '__all__'

class DoctorUpdateSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Doctor
        fields = ['tracks','specialization', 'private_field','phone']



