from rest_framework.permissions import BasePermission


class UserPermissions(BasePermission):
    '''
    Permission class for managing User objects, 
    need to be with IsAuthenticated class.
    '''
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            if user.is_staff:
                return True
                          
            elif view.action in ['list','retrieve','destroy', 
                                 'update', 'partial_update']:
                return True

        
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_authenticated:
            if (obj == user or user.is_staff):
                return True
            
            elif  (obj == user 
                   and view.action in ['retrierve', 'destroy',
                                       'update', 'partial_update']):
                return True
            
            elif (user.usertype == 'c' 
                  and view.action in ['retrieve']):
                return True