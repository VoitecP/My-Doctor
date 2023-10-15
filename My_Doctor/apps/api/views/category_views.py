from apps.core.models import Category
from ..serializers import category_serializers
from ..permissions import IsDirector
from .view_mixins import CategoryQuerysetMixin, CategorySerializerMixin

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response  
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveDestroyAPIView, CreateAPIView, DestroyAPIView





class CategoryListView(CategoryQuerysetMixin, CategorySerializerMixin, ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsDirector]
    # http_method_names = ['get','post','retrieve','put','patch']
    

class CategoryCreateView(CreateAPIView):
      
    """
    View for create Category model
    """
    permission_classes = [IsAdminUser, IsDirector] 


    def get_queryset(self):
        return Category.objects.none()
    
    def get_serializer_class(self):
        return category_serializers.CategoryCreateSerializer

   
class CategoryUpdateView(CategoryQuerysetMixin, CategorySerializerMixin, RetrieveUpdateAPIView):
    """
    View for update Category model
    """
    permission_classes=[IsAdminUser, IsDirector]


    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)            


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

    