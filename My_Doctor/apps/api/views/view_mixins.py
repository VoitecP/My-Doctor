from django.shortcuts import get_object_or_404
from django.views.generic.detail import SingleObjectMixin
from rest_framework.viewsets import   ModelViewSet

from ..serializers.patient_serializers import PatientUpdateSerializer
from ..serializers.doctor_serializers import DoctorUpdateSerializer
from ..serializers.director_serializers import DirectorUpdateSerializer
from ..serializers.category_serializers import CategorySerializer
from apps.core.models import User, Patient, Doctor, Director, Category


class ContextMixin:
    def get_serializer_context(self):
        # is_viewset = False
        # if issubclass(self.__class__, ModelViewSet):
        #     is_viewset = True
        try:
            instance = self.get_object()
        except:
            instance = None
        action = getattr(self, 'action', None)
        context = super().get_serializer_context()
        context.update({
            'request': self.request,   # exist in default
            'action': action,
            'instance': instance,
            # 'is_viewset': is_viewset,
        })
        return context 



####

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
            return CategorySerializer


class VisitQuerysetMixin:

    def get_queryset(self):
        is_admin=self.request.user.is_staff

        # if
        return super().get_queryset()
    


# Todo
## clean Mixins
###

class ContextModelViewSet(ContextMixin, ModelViewSet):
    pass


