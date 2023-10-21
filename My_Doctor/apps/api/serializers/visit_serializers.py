from apps.core.models import Visit
from rest_framework import serializers
from .doctor_serializers import DoctorPublicSerializer, DoctorPrivateSerializer, DoctorVisitSerializer
from .patient_serializers import PatientPublicSerializer, PatientPrivateSerializer, PatientVisitSerializer


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


class VisitPrivateSerializer(serializers.ModelSerializer):
    """
    Patient and doctor can see related visit
    """
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    doctor = DoctorVisitSerializer(read_only=True)
    patient = PatientVisitSerializer(read_only=True)

    class Meta:
        model = Visit
        fields = '__all__'


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
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # doctor = DoctorPublicSerializer(read_only=True)
    # patient = PatientPublicSerializer(read_only=True)

    class Meta:
        model = Visit
        # fields = '__all__'
        fields = ['tracks','title','date','category','description','price','patient','doctor']

    def perform_create(self, validated_data):
        visit = Visit.objects.create(
            validated_data['title'], 
            validated_data['date'], 
            validated_data['patient'],
            validated_data['doctor'],
            validated_data['category'],
            validated_data['description'],
            validated_data['price'])
        visit.title = validated_data['title']
        visit.date = validated_data['date']
        visit.patient = validated_data['patient']
        visit.doctor = validated_data['doctor']
        visit.category = validated_data['category']
        visit.description = validated_data['decsription']
        visit.price = validated_data['price']
        visit.save()
        return visit  


