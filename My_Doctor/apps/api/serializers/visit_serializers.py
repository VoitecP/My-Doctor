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
        # user.is_valid() # checks
        visit.save()
        return visit  


    # id=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    # title=models.CharField(max_length=100, default='')
    # date=models.DateTimeField(default=None, null=True, blank=True)    
    # patient=models.ForeignKey(Patient, models.PROTECT, default=None)
    # doctor=models.ForeignKey(Doctor, models.PROTECT, default=None)
    # category=models.ForeignKey(Category,models.PROTECT,null=True,blank=True, default=None)
    # description=models.TextField()
    # price=models.CharField(max_length=10)



    # def perform_create(self, validated_data):
    #     category = Category.objects.create(
    #         validated_data['name'], 
    #         validated_data['description'])
    #     category.name = validated_data['name']
    #     category.description = validated_data['description']
    #     # category.is_valid() # checks
    #     category.save()
    #     return category