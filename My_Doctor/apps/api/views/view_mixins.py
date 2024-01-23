from django.shortcuts import get_object_or_404
from django.views.generic.detail import SingleObjectMixin
from rest_framework.viewsets import   ModelViewSet
from rest_framework.generics import  (CreateAPIView, 
            ListCreateAPIView, RetrieveUpdateAPIView, DestroyAPIView, 
            RetrieveDestroyAPIView,
            RetrieveUpdateDestroyAPIView)

from ..serializers.patient_serializers import PatientUpdateSerializer
from ..serializers.doctor_serializers import DoctorUpdateSerializer
from ..serializers.director_serializers import DirectorUpdateSerializer
from ..serializers.category_serializers import CategorySerializer
from apps.core.models import User, Patient, Doctor, Director, Category


class ContextMixin:
    def get_serializer_context(self):
        try:
            instance = self.get_object()
        except:
            instance = None
        action = getattr(self, 'action', None)
        request_method = getattr(self.request, 'method', '')
        context = super().get_serializer_context()
        custom_action = self.get_custom_action(instance, action, request_method)
        context.update({
            'request': self.request,   # exist in default
            'action': action,
            'instance': instance,
            'custom_action': custom_action,
        })
        return context 
    
    def get_custom_action(self, instance, action, request_method):

        if action:
            return action
        if bool(request_method == 'GET' and not instance):
            return 'list'
        if bool(request_method == 'POST' and not instance):
            return 'create'
        if bool(request_method == 'GET' and instance):
            return 'retrieve'
        if bool(request_method == 'DELETE' and instance):
            return 'destroy'
        if bool(request_method == 'PUT' and instance):
            return 'update'
        if bool(request_method == 'PATCH' and instance):
            return 'partial_update'
        return ''

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


class ContextListCreateAPIView(ContextMixin, ListCreateAPIView):
    pass


class ContextAPIView(ContextMixin, RetrieveUpdateDestroyAPIView):
    pass


class ContextCreateAPIView(ContextMixin, CreateAPIView):
    pass


class ContextUpdateAPIView(ContextMixin, RetrieveUpdateAPIView):
    pass


class ContextDestroyAPIView(ContextMixin, RetrieveDestroyAPIView):
    pass