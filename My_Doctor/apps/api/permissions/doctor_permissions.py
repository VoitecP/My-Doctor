from rest_framework.permissions import BasePermission


class DoctorPermissions(BasePermission):
    
    def has_permission(self, request, view):
        user = request.user
        if (user.is_authenticated
            and view.action in ['list','retrieve','destroy',
                                'update','partial_update']):
            return True  
           
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_authenticated:   
            if user.is_staff:
                return True
            
            elif  (obj.user == request.user 
                   and view.action in ['retrieve', 'destroy',
                                       'update', 'partial_update']):
                return True
                      
            




