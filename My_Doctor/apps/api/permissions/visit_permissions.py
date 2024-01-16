from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated
from rest_framework.reverse import reverse

from apps.core.models import Patient, User, Doctor, Director


class VisitPermissions(BasePermission):
    '''
    Permission class for managing Visit objects, 
    need to be with IsAuthenticated class.
    '''

    P_METHODS = ('PUT','PATH','POST')
    D_METHODS = ('PUT','PATH',)
    C_METHODS = ('PUT','PATH','POST','DELETE')
    NOT_ALLOWED= ('PUT','PATH','POST','DELETE')
    
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
    
                
            if request.user.usertype =='c' or request.user.is_staff == True:
                if request.method in SAFE_METHODS or self.C_METHODS:
                    return True
            
            else:
                return False
        else:
            return False
        




class VisitPermissions2(BasePermission):
    '''
    Permission class for managing Visit objects, 
    need to be with IsAuthenticated class.
    '''

    P_METHODS = ('PUT','PATH','POST')
    D_METHODS = ('PUT','PATH',)
    C_METHODS = ('PUT','PATH','POST','DELETE')
    NOT_ALLOWED= ('PUT','PATH','POST','DELETE')
    
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.usertype =='p':
                return True
            if request.user.usertype =='d':
                if request.method in SAFE_METHODS:
                    return True
            if request.user.usertype =='c' or request.user.is_staff == True:
                return True
            
            else:
                return False
        else:
            return False

        
    def has_object_permission(self, request, view, obj):

        if request.user.is_authenticated:
            if request.user.usertype =='p':
                if obj.closed == True and request.method in SAFE_METHODS:
                    return True
                if obj.closed == True and request.method in self.NOT_ALLOWED:
                    raise PermissionDenied(f'Visit is closed')
                if obj.closed == False and request.method in SAFE_METHODS or self.P_METHODS:
                    return True
                
            if request.user.usertype =='d':
                if obj.closed == True and request.method in SAFE_METHODS:
                    return True
                if obj.closed == True and request.method in self.NOT_ALLOWED:
                    raise PermissionDenied(f'Visit is closed')
                if obj.closed == False and request.method in SAFE_METHODS or self.D_METHODS:
                    return True
                
            if request.user.usertype =='c' or request.user.is_staff == True:
                if request.method in SAFE_METHODS or self.C_METHODS:
                    return True
            
            else:
                return False
        else:
            return False
        