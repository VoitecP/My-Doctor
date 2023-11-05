from apps.core.models import PatientPhotoFile
from rest_framework import serializers
# from apps.api.serializers import UserPublicSerializer, UserPrivateSerializer, UserVisitSerializer

from rest_framework.response import Response 
from rest_framework.serializers import ValidationError



class PatientPhotoSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = PatientPhotoFile
        # fields = ['image']
        fields = '__all__'

        


class PatientPhotoCreateSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = PatientPhotoFile
        fields = ['image','tracks']
        # fields = '__all__'

    def perform_create(self, validated_data):
        try:
            photo = PatientPhotoFile.objects.create(
            validated_data['image'])
            photo.user = self.request.user
            photo.image = validated_data['image']
            photo.save()
            return photo
        except:
            raise ValidationError({"detail": "Operation not allowed"})