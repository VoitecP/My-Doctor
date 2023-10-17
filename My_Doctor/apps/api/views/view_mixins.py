from apps.core.models import User, Patient, Doctor, Director, Category
from ..serializers.patient_serializers import PatientUpdateSerializer
from ..serializers.doctor_serializers import DoctorUpdateSerializer
from ..serializers.director_serializers import DirectorUpdateSerializer
from ..serializers.category_serializers import CategoryPublicSerializer
from django.shortcuts import get_object_or_404
from django.views.generic.detail import SingleObjectMixin

# class UUIDMixin(SingleObjectMixin):
    
#     def get_object(self):
#         return self.model.objects.get(id=self.kwargs.get("id"))


class UserQuerysetMixin:

    def get_queryset(self):
        usertype=self.request.user.usertype
        if usertype == 'p':
            return Patient.objects.filter(user=self.request.user)  # replace to get_object.. or 404
        if usertype == 'd':
            return Doctor.objects.filter(user=self.request.user)
        if usertype == 'c':
            return Doctor.objects.filter(user=self.request.user)
        


class UserObjectMixin:

    def get_object(self):
        usertype=self.request.user.usertype
        if usertype == 'p':
            return get_object_or_404(Patient, user=self.request.user)
        if usertype == 'd':
            return get_object_or_404(Doctor, user=self.request.user)
        if usertype == 'c':
            return get_object_or_404(Director, user=self.request.user)

class UserSerializerMixin:

    def get_serializer_class(self):
        usertype=self.request.user.usertype
        if usertype == 'p':
            return PatientUpdateSerializer
        if usertype == 'd':
            return DoctorUpdateSerializer
        if usertype == 'c':
            return DirectorUpdateSerializer



class CategoryQuerysetMixin:

    def get_queryset(self):
            return Category.objects.all()
        

class CategorySerializerMixin:

    def get_serializer_class(self):
            return CategoryPublicSerializer


class VisitQuerysetMixin:

    def get_queryset(self):
        is_admin=self.request.user.is_staff

        # if
        return super().get_queryset()
    