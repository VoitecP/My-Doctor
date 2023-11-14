from apps.core.models import VisitImageFile
from rest_framework import serializers
# from apps.api.serializers import UserPublicSerializer, UserPrivateSerializer, UserVisitSerializer

from rest_framework.response import Response 
from rest_framework.serializers import ValidationError

class VisitImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitImageFile
        fields = ['id','title','image_url','thumb_url']



class PatientImageSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = VisitImageFile
        # fields = ['image']
        fields = '__all__'

        


class PatientImageCreateSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = VisitImageFile
        fields = ['image','tracks']
        # fields = '__all__'

    def perform_create(self, validated_data):
        try:
            image = VisitImageFile.objects.create(
            validated_data['image'])
            image.user = self.request.user
            image.image = validated_data['image']
            image.save()
            return image
        except:
            raise ValidationError({"detail": "Operation not allowed"})
        

class PatientImageDeleteSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = VisitImageFile
        # ields = ['image','tracks']
        fields = '__all__'

    