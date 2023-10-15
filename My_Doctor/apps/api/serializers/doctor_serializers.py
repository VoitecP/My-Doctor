from apps.core.models import Doctor
from rest_framework import serializers
# from apps.api.serializers import UserPublicSerializer, UserPrivateSerializer, UserVisitSerializer
from apps.api.serializers import user_serializers


class DoctorPublicSerializer(serializers.ModelSerializer):
    """
    All users can view this fields
    """
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    user = user_serializers.UserPublicSerializer(read_only=True)
    
    class Meta:
        model = Doctor
        fields = ['user','specialization','tracks']
        # fields = '__all__'
         

class DoctorPrivateSerializer(serializers.ModelSerializer):
    """
    Only logged user can view these fields , self fields.
    """
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    user = user_serializers.UserPrivateSerializer(read_only=True)
    
    class Meta:
        model = Doctor
        fields = ['user','specialization','private_field','tracks']


class DoctoVisitSerializer(serializers.ModelSerializer):
    """
    Only connected thru common visit can see these fields
    """
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    user = user_serializers.UserVisitSerializer(read_only=True)
    
    class Meta:
        model = Doctor
        fields = ['user','specialization','tracks']
         

####

#  Not need

# class DoctorSerializer(serializers.ModelSerializer):
#     tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
#     class Meta:
#         model = Doctor
#         fields = '__all__'


class DoctorUpdateSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Doctor
        fields = ['tracks','specialization', 'private_field','phone']
        # fields = '__all__'



