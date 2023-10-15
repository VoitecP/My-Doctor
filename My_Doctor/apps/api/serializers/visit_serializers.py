from apps.core.models import Visit
from rest_framework import serializers
from .doctor_serializers import DoctorPublicSerializer, DoctorPrivateSerializer, DoctoVisitSerializer
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
        fields =['tracks','patient','doctor','price']

# id=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
#     title=models.CharField(max_length=100, default='')
#     date=models.DateTimeField(default=None, null=True, blank=True)    
#     patient=models.ForeignKey(Patient, models.PROTECT, default=None)
#     doctor=models.ForeignKey(Doctor, models.PROTECT, default=None)
#     category=models.ForeignKey(Category,models.PROTECT,null=True,blank=True, default=None)
#     description=models.TextField()
#     price=models.CharField(max_length=10)



class VisitPrivateSerializer(serializers.ModelSerializer):
    """
    Patient and doctor can see related visit
    """
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    doctor = DoctorPublicSerializer(read_only=True)
    patient = PatientPublicSerializer(read_only=True)


    class Meta:
        model = Visit
        fields = '__all__'


##

class VisitUpdateSerializer(serializers.ModelSerializer):
    """
    Patient and doctor can see related visit
    """
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    doctor = DoctorPublicSerializer(read_only=True)
    patient = PatientPublicSerializer(read_only=True)

    class Meta:
        model = Visit
        fields = '__all__'


# No need this visit

# class VisitVisitSerializer(serializers.ModelSerializer):
#     tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
#     doctor = DoctorPublicSerializer(read_only=True)
#     patient = PatientPublicSerializer(read_only=True)

#     class Meta:
#         model = Visit
#         fields = '__all__'


###


# class LoginUserSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(write_only=True, required=True)
#     password = serializers.CharField(write_only=True, required=True)
    
#     class Meta:
#         model = User
#         fields = ['username', 'password']


# class DoctorPublicSerializer(serializers.ModelSerializer):
#     tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
#     user = UserPublicSerializer(read_only=True)
    
#     class Meta:
#         model = Doctor
#         fields = ['tracks','user','specialization','phone']
#         # fields = '__all__'