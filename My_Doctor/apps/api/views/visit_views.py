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

class Visit2Viewset(ModelViewSet):

    # TODO None type of user , gives error need permission.
    
    # queryset=Visit.objects.all()
    #serializer_class=visit_serializers.VisitViewsetSerializer

    def get_queryset(self):
        usertype=self.request.user.usertype
        is_superuser=self.request.user.is_superuser
        id=self.request.user.id

        if is_superuser == True:        #or maybe disable?
            return Visit.objects.all()     
        else:
            if usertype == 'p':
                # return Visit.objects.filter(patient__pk=id)
                return Visit.objects.all()    
            if usertype == 'd':
                return Visit.objects.filter(doctor__pk=id)
            if usertype == 'c':
                return Visit.objects.all()




    def get_serializer_class(self):
        usertype=self.request.user.usertype

        if usertype == 'p':
            if self.action == ('list'):
                #  url,  patient/doctor/description/date..
                #  VisitListPTypeSerializer
                return visit_serializers.VisitListPTypeSerializer
            if self.action  in ('retrieve', 'create', 'destroy'):
                # url   full list
                # VisitRetrievePTypeSerializer
                # return visit_serializers.VisitViewsetSerializer
                return visit_serializers.VisitRetrievePTypeSerializer
            if self.action in ('update','partial_update'):
                # return visit_serializers.VisitViewsetSerializer
                return visit_serializers.VisitUpdatePTypeSerializer
            
            pass
            pass
        
        if usertype == 'd':
            pass

        if usertype == 'c':
            pass

        if self.action == 'list':
            return visit_serializers.VisitViewsetSerializer
        if self.action  in ('create', 'retrieve','destroy'):
            pass
        if self.action == 'retrieve':
            pass
            #if self.context.closed == True:
            #if self.context['request'].visit.closed == True:
            return visit_serializers.VisitViewsetSerializer
        if self.action in ('update','partial_update'):

            pass
        if self.action == 'destroy':
            pass
        # else:
        #         return visit_serializers.VisitViewsetSerializer
            
        else:
            return visit_serializers.VisitViewsetSerializer  # must be default serializer

class VisitViewset(ModelViewSet):
    """
    Visit model List View (filtered list view)
    """
    #permission_classes=[VisitPermissions, TypeUpdatedPermission]
    #permission_classes=[VisitPermissions]

    # permission_classes=[IsPatientOrReadOnly]

    queryset=Visit.objects.all()
    serializer_class=visit_serializers.VisitViewsetSerializer
    
    
    def get_dqueryset(self):
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
                # return Visit.objects.all()
            if usertype == 'c':
                return Visit.objects.all()

    def get_dserializer_class(self):
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
        

    # if self.action == 'list':
    #         return serializers.ListaGruppi
    #     if self.action == 'retrieve':
    #         return serializers.DettaglioGruppi
    #     return serializers.Default # I dont' know what you want for create/destroy/update.           


# nippet_list = SnippetViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })
# snippet_detail = SnippetViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# })
# snippet_highlight = SnippetViewSet.as_view({
#     'get': 'highlight'
# }, renderer_classes=[renderers.StaticHTMLRenderer])
# user_list = UserViewSet.as_view({
#     'get': 'list'
# })
# user_detail = UserViewSet.as_view({
#     'get': 'retrieve'
# })


#  def list(self, request):
#         pass

#     def create(self, request):
#         pass

#     def retrieve(self, request, pk=None):
#         pass

#     def update(self, request, pk=None):
#         pass

#     def partial_update(self, request, pk=None):
#         pass

#     def destroy(self, request, pk=None):
#         pass


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
    