from rest_framework.permissions import BasePermission

from ..views.view_mixins import ContextMixin


class UserPermissions(BasePermission):
    '''
    Permission class for managing User objects, 
    need to be with IsAuthenticated class.
    '''
    
    def has_permission(self, request, view):
        user = request.user
        action = getattr(view, 'action', None)
        method = request.method
        custom_action = ContextMixin.get_custom_action(
                self, instance=None, action=action, request_method=method)
            
        if user.is_authenticated:
            if user.is_staff:
                return True              
            elif custom_action not in 'create':
                return True
        
        
    def has_object_permission(self, request, view, obj):
        user = request.user
        action = getattr(view, 'action', None)
        method = request.method
        custom_action = ContextMixin.get_custom_action(
                self, instance=obj, action=action, request_method=method)

        if user.is_authenticated:
            if (obj == user or user.is_staff):
                return True
    
            elif (obj == user and custom_action
                                in ['retrierve', 'destroy',
                                    'update', 'partial_update']):
                return True
            
            elif (user.usertype == 'c' and custom_action 
                                        in ['retrieve']):
                return True