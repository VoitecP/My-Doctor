from rest_framework.permissions import BasePermission, SAFE_METHODS
from apps.core.models import Patient, User, Doctor, Director
from rest_framework.reverse import reverse
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

class BaseObjectPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:      # Read permissions are allowed to any request 
            return True
        return obj.user == request.user          # Write permissions are only allowed to the user


class DirectorSingletonPermission(BaseObjectPermission):
    message='Director sigleton instance'

    def has_permission(self, request, view):
        if Director.objects.exists():
            return False

class ModelExistsPermission(BaseObjectPermission):
    # Not need more
    patient_status=False
    doctor_status=False
    director_status=False
    ##
    return_status=False

    def has_permission(self, request, view):
        if bool (request.user and request.user.is_authenticated):
            if Patient.objects.filter(user=request.user).exists():
                return self.patient_status
            if Doctor.objects.filter(user=request.user).exists():
                return self.doctor_status
            if Director.objects.filter(user=request.user).exists():
                return self.director_status
        return self.return_status

class TypeCreatedPermission(BaseObjectPermission):
# Proparbly not need because it will automatic create models.
   
    def has_permission(self, request, view):
        if (request.user.is_authenticated 
            and request.user.is_staff == False
            and request.user.type_created == True):
            return True
        else:
            return False
    

class TypeUpdatedPermission(BasePermission):

    def url_pattern(self, request):
    
        if request.user.usertype == 'p':
            pattern = 'api:patient-detail'
        if request.user.usertype == 'd':
            pattern = 'api:doctor-detail'
        if request.user.usertype == 'c':
            pattern = 'api:director-detail'
        
        return reverse(pattern, 
                    kwargs={"pk": request.user.pk}, 
                    request=request)
        

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if (request.user.is_staff == False
                and request.user.type_created == True
                and request.user.type_updated == False):
                return True
            else:
                url=self.url_pattern(request)
                raise PermissionDenied(f'Update Your profile here: {url}')
        else:
            raise PermissionDenied(f'Please Login:')
        



class UserTypePermission(BaseObjectPermission):
    usertype = None   

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.usertype == self.usertype:
                return True
        return False 


class IsNotUserUpdated(ModelExistsPermission):
    patient_status=False
    doctor_status=False
    director_status=False
    ##
    return_status=True


class IsUserUpdated(ModelExistsPermission):
    patient_status=True
    doctor_status=True
    director_status=True
    ##
    return_status=False



class IsPatient(UserTypePermission):
    usertype = 'p'


class IsDoctor(UserTypePermission):
    usertype = 'd'


class IsDirector(UserTypePermission):
    usertype = 'c'


class IsPatientCreated(ModelExistsPermission):
    patient_status=True
    doctor_status=False
    director_status=False
    ##
    return_status=False


class IsDoctorCreated(ModelExistsPermission):
    patient_status=False
    doctor_status=True
    director_status=False
    ##
    return_status=False


class IsDirectorCreated(ModelExistsPermission):
    patient_status=False
    doctor_status=False
    director_status=True
    ##
    return_status=False


class IsUserTypeOrReadOnly(BasePermission):
    usertype=None
    
    def has_permission(self, request, view):

        if request.user.is_authenticated:
            if request.method in SAFE_METHODS:
                return True
        
            elif (request.user.usertype == self.usertype
               and request.user.is_authenticated):
                return True
        else:
            return False
    
class IsDirectorOrReadOnly(IsUserTypeOrReadOnly):
    usertype='d'


class IsPatientOrReadOnly(IsUserTypeOrReadOnly):
    usertype='p'



class CategoryPermissions(BasePermission):
    '''
    Permission class for managing Category objects, need to be with IsAuthenticated class.
    '''

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.usertype =='p' or request.user.usertype =='d':
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
            if request.user.usertype =='p' or request.user.usertype =='d':
                if request.method in SAFE_METHODS:
                    return True
                if request.method in self.NOT_ALLOWED:
                    raise PermissionDenied(f'You are not allowed to this operation')
                
    
            if request.user.usertype =='c' or request.user.is_staff == True:
                return True
            
            else:
                return False
        else:
            return False
                
    

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
        


class DirectorPermissions(BasePermission):
    '''
    Permission class for managing Director objects, 
    need to be with IsAuthenticated class.
    '''
    NOT_ALLOWED = ('PUT','PATH','POST','DELETE')
    ALLOWED = ('PUT','PATH','DELETE')
    
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.usertype in ['p','d']:

                if request.method in SAFE_METHODS:
                    return True            
                    
                if request.method in self.NOT_ALLOWED:
                    raise PermissionDenied(f'Method not allowed')
                
            if (request.user.usertype =='c' or request.user.is_staff == True):
                 
                 if (request.method in SAFE_METHODS or 
                     request.method in self.ALLOWED):
                    return True
            
            else:
                return False
        else:
            return False

        
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:

            if request.user.usertype in ['p', 'd']:
                if request.method in SAFE_METHODS:
                    return True
                
            if (request.user.usertype =='c' or request.user.is_staff == True):

                if (request.method in SAFE_METHODS or 
                     request.method in self.ALLOWED):
                    return True
                
            else:
                return False
        else:
            return False
          



class DoctorPermissions(BasePermission):
    '''
    Permission class for managing Doctor objects, 
    need to be with IsAuthenticated class.
    '''
    # TODO rewrite permissions to view.actions in Views/Viewsets
    NOT_ALLOWED = ('PUT','PATH','POST','DELETE')
    ALLOWED = ('PUT','PATH','DELETE')
    
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.usertype in ['p','d']:

                if request.method in SAFE_METHODS:
                    return True            
                    
                if request.method in self.NOT_ALLOWED:
                    raise PermissionDenied(f'Method not allowed')
                
            if (request.user.usertype =='c' or request.user.is_staff == True):
                 
                 if (request.method in SAFE_METHODS or 
                     request.method in self.ALLOWED):
                    return True
            
            else:
                return False
        else:
            return False

        
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:

            if request.user.usertype in ['p', 'd']:
                if request.method in SAFE_METHODS:
                    return True
                
            if (request.user.usertype =='c' or request.user.is_staff == True):

                if (request.method in SAFE_METHODS or 
                     request.method in self.ALLOWED):
                    return True
                
            else:
                return False
        else:
            return False
          


class UserPermissions(BasePermission):
    '''
    Permission class for managing User objects, 
    need to be with IsAuthenticated class.
    '''
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if (request.user.usertype == 'c' or request.user.is_staff):
                return True
                          
            elif view.action in ['list','retrieve','destroy', 
                                 'update', 'partial_update']:
                return True

            else:
                return False          
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if (request.user.usertype == 'c' or request.user.is_staff):
                return True
            
            elif  (obj == request.user 
                   and view.action in ['retrierve', 'destroy',
                                       'update', 'partial_update']):
                return True
            
            else:
                return False    
        else:
            return False
     