from rest_framework.decorators import action
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveDestroyAPIView,UpdateAPIView, CreateAPIView, ListCreateAPIView
from rest_framework.response import Response  
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.viewsets import ModelViewSet, GenericViewSet,  ReadOnlyModelViewSet
from rest_framework.serializers import ValidationError

from ..permissions import *
from ..serializers import visit_serializers
from .view_mixins import ContextModelViewSet
from apps.core.models import Visit
# from ..permissions import IsDoctorCreated, IsPatientCreated, IsNotUserUpdated
# from .view_mixins import UserQuerysetMixin, UserObjectMixin, UserSerializerMixin


#####
# Viewsets
#####

class VisitViewSet(ContextModelViewSet):

    # TODO None type of user , gives error need permission.
    # permission_classes=[IsAuthenticated, VisitPermissions]
    queryset = Visit.objects.all()
    serializer_class = visit_serializers.VisitDynamicSerializer

    def get_querysett(self):
        user=self.request.user

        if user.usertype == 'p':
            return Visit.objects.filter(patient__pk=user.id)
            
        elif user.usertype == 'd':
            return Visit.objects.filter(doctor__pk=user.id)
            
        elif (user.usertype == 'c' or user.is_staff == True):
            return Visit.objects.all()
        else:
            return Visit.objects.none()


    def get_serializer_classs(self):
        usertype=self.request.user.usertype
        is_staff=self.request.user.is_staff

        if usertype == 'p':
            if self.action == 'list':
                # Todo url,  patient/doctor/description/date..
                return visit_serializers.VisitListSerializerForPatient
            if self.action  in ['retrieve', 'create', 'destroy']:
                # TODO url   full list
                # return visit_serializers.VisitViewsetSerializer
                return visit_serializers.VisitRetrieveSerializerForPatient
            if self.action in ['update','partial_update']:
                # return visit_serializers.VisitViewsetSerializer
                return visit_serializers.VisitUpdateSerializerForPatient   
            
            else:
                return visit_serializers.VisitListSerializerForPatient   
            
        if usertype == 'd':
            if self.action == ['list']:
                #  url,  patient/doctor/description/date..
                return visit_serializers.VisitListSerializerForDoctor
            if self.action  in ['retrieve', 'create', 'destroy']:
                return visit_serializers.VisitRetrieveSerializerForDoctor
            if self.action in ['update','partial_update']:
                return visit_serializers.VisitUpdateSerializerForDoctor
            
            else:
                return visit_serializers.VisitListSerializerForDoctor
        
        if usertype == 'c' or is_staff == True:
            if self.action == 'list':
                #  url,  patient/doctor/description/date..
                return visit_serializers.VisitListSerializerForDirector
            if self.action  in ['retrieve', 'create', 'destroy']:
                return visit_serializers.VisitRetrieveSerializerForDirector
            if self.action in ['update','partial_update']:
                return visit_serializers.VisitUpdateSerializerForDirector
            
            else:
                return visit_serializers.VisitListSerializerForDirector
        
        else:
            return visit_serializers.VisitListSerializerForPatient  # must be default serializer



    

class VisitViewset2(ModelViewSet):

    # TODO None type of user , gives error need permission.
    permission_classes=[IsAuthenticated, VisitPermissions]
    # permission_classes=[AllowAny, VisitPermissions]
    # queryset = Visit.objects.all()

    def get_queryset(self):
        usertype=self.request.user.usertype
        is_staff=self.request.user.is_staff
       

        if usertype == 'p':
            #TODO  replace to filter by id when finished
            return Visit.objects.filter(patient__pk=id)
              
        if usertype == 'd':
             return Visit.objects.filter(doctor__pk=id)
           
        if usertype == 'c' or is_staff == True:
            return Visit.objects.all()
        else:
            return Visit.objects.all()


    def get_serializer_class(self):
        usertype=self.request.user.usertype
        is_staff=self.request.user.is_staff

        if usertype == 'p':
            if self.action == 'list':
                # Todo url,  patient/doctor/description/date..
                return visit_serializers.VisitListSerializerForPatient
            if self.action  in ['retrieve', 'create', 'destroy']:
                # TODO url   full list
                # return visit_serializers.VisitViewsetSerializer
                return visit_serializers.VisitRetrieveSerializerForPatient
            if self.action in ['update','partial_update']:
                # return visit_serializers.VisitViewsetSerializer
                return visit_serializers.VisitUpdateSerializerForPatient   
            
            else:
                return visit_serializers.VisitListSerializerForPatient   
            
        if usertype == 'd':
            if self.action == ['list']:
                #  url,  patient/doctor/description/date..
                return visit_serializers.VisitListSerializerForDoctor
            if self.action  in ['retrieve', 'create', 'destroy']:
                return visit_serializers.VisitRetrieveSerializerForDoctor
            if self.action in ['update','partial_update']:
                return visit_serializers.VisitUpdateSerializerForDoctor
            
            else:
                return visit_serializers.VisitListSerializerForDoctor
        
        if usertype == 'c' or is_staff == True:
            if self.action == 'list':
                #  url,  patient/doctor/description/date..
                return visit_serializers.VisitListSerializerForDirector
            if self.action  in ['retrieve', 'create', 'destroy']:
                return visit_serializers.VisitRetrieveSerializerForDirector
            if self.action in ['update','partial_update']:
                return visit_serializers.VisitUpdateSerializerForDirector
            
            else:
                return visit_serializers.VisitListSerializerForDirector
        
        else:
            return visit_serializers.VisitListSerializerForPatient  # must be default serializer


#####
# API Views
#####


class VisitCreateView(ListCreateAPIView):
    """
    View for create Visit model
    """
    permission_classes = [IsAuthenticated] #, IsAdminUser]   it can make errors

    def get_queryset(self):
        return Visit.objects.all()  
        # return Visit.objects.all() 


    def get_serializer_class(self):
        return visit_serializers.VisitCreateSerializer    

    def perform_create(self, serializer):
        try:
            serializer.save()
            return Response({"detail": "Success"})
        except:
            raise ValidationError({"detail": "Operation not allowed"})


class VisitUpdateView(RetrieveUpdateAPIView):
    """
    View for update Visit model
    """
    permission_classes=[IsAuthenticated, IsAdminUser]
   
    def get_serializer_class(self):
        return visit_serializers.VisitUpdateSerializer

    # def path(self, request, *args, **kwargs):
    #     return self.partial_update(request, *args, **kwargs)
      

class VisitDeleteView(RetrieveDestroyAPIView):
    """
    View for Delete Visit model
    """
    permission_classes=[IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        return Visit.objects.none()
   
    def get_serializer_class(self):
        return visit_serializers.VisitDeleteSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            visit = self.get_object()
            self.perform_destroy(visit)
            return Response({"detail": "Visit deleted"})
        except:
           return Response({"detail": "User Cannot be deleted"})
    