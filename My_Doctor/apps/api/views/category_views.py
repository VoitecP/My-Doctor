from rest_framework.permissions import IsAuthenticated

from ..serializers import CategoryDynamicSerializer
from ..permissions import CategoryPermissions
from ..views.view_mixins import (ContextAPIView, 
                     ContextListCreateAPIView, 
                     ContextModelViewSet) 
from apps.core.models import Category


class CategoryMixin:

    permission_classes = [IsAuthenticated, CategoryPermissions]
    queryset = Category.objects.all()
    serializer_class = CategoryDynamicSerializer
    
   
class CategoryViewSet(CategoryMixin, ContextModelViewSet):
    '''
    '''
    pass

class CategoryListCreateView(CategoryMixin, ContextListCreateAPIView):
    """
    """
    pass


class CategoryAPIView(CategoryMixin, ContextAPIView):
    """
    """
    pass


