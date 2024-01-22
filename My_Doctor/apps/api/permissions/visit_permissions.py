from rest_framework.permissions import BasePermission
from ..views.view_mixins import ContextMixin

class VisitPermissions(BasePermission):
    '''
    Permission class for managing Visit objects, 
    need to be with IsAuthenticated class.
    '''

    def has_permission(self, request, view):
        user = request.user
        action = getattr(view, 'action', None)
        method = request.method
        custom_action = ContextMixin.get_custom_action(
                self, instance=None, action=action, request_method=method)

        if user.is_authenticated:
            if user.usertype in ['p','c'] or user.is_staff:
                return True
            if user.usertype == 'd' and custom_action not in 'create':
                return True

        
    def has_object_permission(self, request, view, obj):
        user = request.user
        action = getattr(view, 'action', None)
        method = request.method
        custom_action = ContextMixin.get_custom_action(
                self, instance=obj, action=action, request_method=method)
        
        if user.is_authenticated:
            if user.usertype in ['p','d']:
                if (obj.closed and custom_action in ['list','retrieve']):
                    return True
                if not obj.closed:
                    return True   
            if user.usertype =='c' or user.is_staff:
                    return True
            
            
