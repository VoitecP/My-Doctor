from rest_framework.permissions import BasePermission


class FilePermissions(BasePermission):
    '''
    '''
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            if user.is_staff:
                return True
                          
            elif view.action in ['list','create', 
                                 'retrieve','destroy']:
                return True

        
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_authenticated:
            if (obj == user or user.is_staff):
                return True
            
            elif  (user.usertype == 'p' 
                   and view.action in ['retrieve', 'destroy']):
                return True
            
            elif  (user.usertype == 'd' 
                   and view.action in ['retrieve']):
                return True
            
            