from apps.core.models import User, Patient, Doctor, Director
from ..serializers.patient_serializers import PatientUpdateSerializer
from ..serializers.doctor_serializers import DoctorUpdateSerializer
from ..serializers.director_serializers import DirectorUpdateSerializer
from django.shortcuts import get_object_or_404

class QuerysetMixin:

    def get_queryset(self):
        usertype=self.request.user.usertype
        if usertype == 'p':
            return Patient.objects.filter(user=self.request.user)  # replace to get_object.. or 404
        if usertype == 'd':
            return Doctor.objects.filter(user=self.request.user)
        if usertype == 'c':
            return get_object_or_404(Director, user=self.request.user)

class ObjectMixin:

    def get_object(self):
        usertype=self.request.user.usertype
        if usertype == 'p':
            return get_object_or_404(Patient, user=self.request.user)
        if usertype == 'd':
            return get_object_or_404(Doctor, user=self.request.user)
        if usertype == 'c':
            return get_object_or_404(Director, user=self.request.user)

class SerializerMixin:

    def get_serializer_class(self):
        usertype=self.request.user.usertype
        if usertype == 'p':
            return PatientUpdateSerializer
        if usertype == 'd':
            return DoctorUpdateSerializer
        if usertype == 'c':
            return DirectorUpdateSerializer
