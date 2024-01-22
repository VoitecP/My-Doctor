from rest_framework.permissions import BasePermission

from ..views.view_mixins import ContextMixin


class DoctorPermissions(BasePermission):
    
    def has_permission(self, request, view):
        user = request.user
        action = getattr(view, 'action', None)
        method = request.method
        custom_action = ContextMixin.get_custom_action(
                self, instance=None, action=action, request_method=method)
        
        if user.is_authenticated and custom_action not in 'create':
            return True  
           
           
    def has_object_permission(self, request, view, obj):
        user = request.user
        action = getattr(view, 'action', None)
        method = request.method
        custom_action = ContextMixin.get_custom_action(
                self, instance=obj, action=action, request_method=method)
        
        if user.is_authenticated:   
            if user.is_staff:
                return True
            
            elif  (obj.user == request.user 
                    and custom_action not in ['list','create']):
                return True
                      
            




