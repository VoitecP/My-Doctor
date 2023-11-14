from apps.core.models import Visit, Patient, Doctor, Director
from ..serializers import visit_serializers
from ..permissions import *
# from ..permissions import IsDoctorCreated, IsPatientCreated, IsNotUserUpdated
# from .view_mixins import UserQuerysetMixin, UserObjectMixin, UserSerializerMixin


from rest_framework.response import Response  
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveDestroyAPIView,UpdateAPIView, CreateAPIView, ListCreateAPIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet,  ReadOnlyModelViewSet
from rest_framework.serializers import ValidationError



class VisitListView(ModelViewSet):
    """
    Visit model List View (filtered list view)
    """
    # permission_classes=[IsAuthenticated, IsAdminUser, IsDirector]

    # queryset=Visit.objects.all()
    
    
    def get_queryset(self):
        usertype=self.request.user.usertype
        is_superuser=self.request.user.is_superuser
        id=self.request.user.id

        if is_superuser == True:
            return Visit.objects.all()     
        else:
            if usertype == 'p':
                return Visit.objects.filter(patient__pk=id)   
            if usertype == 'd':
                return Visit.objects.filter(doctor__pk=id)
            if usertype == 'c':
                return Visit.objects.all()

    def get_serializer_class(self):
        usertype=self.request.user.usertype
        is_superuser=self.request.user.is_superuser
        id=self.request.user.id

        if is_superuser == True:
            return visit_serializers.VisitViewsetSerializer 
        else:  
            if usertype == 'p':
                return visit_serializers.VisitViewsetSerializer   
            if usertype == 'd':
                return visit_serializers.VisitPublicSerializer
            if usertype == 'c':
                return visit_serializers.VisitPublicSerializer
        

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
    