from apps.core.models import Category
from ..serializers import category_serializers
from ..permissions import CategoryPermissions, IsDirector, IsDirectorOrReadOnly
from .view_mixins import CategoryQuerysetMixin, CategorySerializerMixin
from rest_framework import status

from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.response import Response 
from rest_framework.exceptions import MethodNotAllowed 
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveDestroyAPIView, ListCreateAPIView, DestroyAPIView
from rest_framework.serializers import ValidationError

#####
# Viewsets
#####

class CategoryViewset(ModelViewSet):
  
    permission_classes=[IsAuthenticated, CategoryPermissions]

    def get_queryset(self):
            return Category.objects.all()
        

    def get_serializer_class(self):
        usertype=self.request.user.usertype
        is_staff=self.request.user.is_staff

        if usertype == 'c' or is_staff == True:
            return category_serializers.CategoryDirectorSerializer
        else:
            return category_serializers.CategorySerializer

    
#####
# API Views
#####        


class CategoryCreateView(ListCreateAPIView):
    """
    View for create Category model
    """
    permission_classes = [IsAdminUser, IsDirector] 


    def get_queryset(self):
        return Category.objects.none()
    
    def get_serializer_class(self):
        return category_serializers.CategoryCreateSerializer
    
    def perform_create(self, serializer):
        try:
            serializer.save()
            return Response({"detail": "Success"})
        except:
            raise ValidationError({"detail": "Operation not allowed"})

   
class CategoryUpdateView(CategoryQuerysetMixin, CategorySerializerMixin, RetrieveUpdateAPIView):
    """
    View for update Category model
    """
    permission_classes=[IsAdminUser, IsDirector]

    # def put(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)            


class CategoryDeleteView(CategoryQuerysetMixin, CategorySerializerMixin, RetrieveDestroyAPIView): 
    """
    View for pernament delete User model
    """
    permission_classes = [IsAdminUser, IsDirector]
    
    def delete(self, request, *args, **kwargs):
        try:
            self.destroy(request, *args, **kwargs)
            return Response({"detail": "Category deleted succesfull"})
        except:
            return Response({"detail": "Category cannot be deleted"})

    