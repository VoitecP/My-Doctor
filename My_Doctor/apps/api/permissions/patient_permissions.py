from rest_framework.permissions import BasePermission


class PatientPermissions(BasePermission):
    '''
    Permission class for managing Patient objects, 
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
            if (obj.user == user or user.is_staff):
                return True
            
            elif  (obj.user == user 
                   and view.action in ['retrieve', 'destroy',
                                       'update', 'partial_update']):
                return True
            
            elif (user.usertype in ['d','c'] 
                  and view.action in ['retrieve']):
                return True