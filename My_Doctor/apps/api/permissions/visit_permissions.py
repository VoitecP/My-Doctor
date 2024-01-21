from rest_framework.permissions import BasePermission
from ..serializers.serializer_mixins import DynamicMixin


class VisitPermissions(BasePermission):
    '''
    Permission class for managing Visit objects, 
    need to be with IsAuthenticated class.
    '''
    def has_permission(self, request, view):
        user = request.user
        method = request.method
        action = getattr(view, 'action', None)


        if user.is_authenticated:
            if user.usertype in ['p','c'] or user.is_staff:
                return True
            
            # if (action user.usertype == 'd' 
            #     and (action  and action not 'create')):
            #     return True


            if (action in ['list','retrieve',
                                'destroy', 'update',
                                'partial_update'] 
                or method in ['GET','DELETE','PUT','PATCH']):
                return True
            
        
    def has_object_permission(self, request, view, obj):
        user = request.user
        method = request.method
        action = getattr(view, 'action', None)
        
        if user.is_authenticated:
            if user.usertype in ['p','d']:
                if (obj.closed and action in ['list','retrieve']
                    or method == 'GET'):
                    return True
                if not obj.closed:
                    return True
                
            if user.usertype =='c' or user.is_staff:
                    return True
            
            