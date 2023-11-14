from apps.core.models import Doctor
from rest_framework import serializers, reverse

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


class DoctorVisitSerializer(serializers.ModelSerializer):
    """
    Only connected thru common visit can see these fields
    """

    first_name=serializers.SerializerMethodField(label='first name', read_only=True)
    last_name=serializers.SerializerMethodField(label='last name', read_only=True)
    email=serializers.SerializerMethodField(read_only=True)
    #url=

    
    class Meta:
        model = Doctor
        fields = ['first_name','last_name', 'email','specialization']

    # def get_url(self, obj):
    #     return obj.url
    
    def get_first_name(self, obj):
        return obj.user.first_name
    
    def get_last_name(self, obj):
        return obj.user.last_name
    
    def get_email(self, obj):
        return obj.user.email



    







class DoctorUpdateSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Doctor
        fields = ['tracks','specialization', 'private_field','phone']
        # fields = '__all__'



