from rest_framework.permissions import BasePermission


class VisitPermissions(BasePermission):
    '''
    Permission class for managing Visit objects, 
    need to be with IsAuthenticated class.
    '''
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:

            if user.usertype in ['p','c'] or user.is_staff:
                return True
            
            if view.action in ['list','retrieve','destroy', 
                                 'update', 'partial_update']:
                return True
            
        
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_authenticated:

            if user.usertype in ['p','d']:
                if obj.closed and view.action in ['list','retrieve']:
                    return True
                
                if not obj.closed:
                    return True
                
            if request.user.usertype =='c' or request.user.is_staff:
                    return True
            
            