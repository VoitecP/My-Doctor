from rest_framework.permissions import BasePermission


class CategoryPermissions(BasePermission):
   
    def has_permission(self, request, view):
        user = request.user

        if user.is_authenticated:
            if user.usertype == 'c' or user.is_staff:
                return True    
                       
            elif (user.usertype in ['p','d'] 
                   and view.action in ['list','retrieve']):
                return True
           
    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.is_authenticated:
            if user.usertype == 'c' or user.is_staff:
                return True  
            
            elif (user.usertype in ['p','d'] 
                   and view.action in ['list','retrieve']):
                return True

