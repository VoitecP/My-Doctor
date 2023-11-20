from rest_framework.permissions import BasePermission, SAFE_METHODS
from apps.core.models import Patient, User, Doctor, Director


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
    patient_status=False
    doctor_status=False
    director_status=False
    ##
    return_status=False

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if Patient.objects.filter(user=request.user).exists():
                return self.patient_status
            if Doctor.objects.filter(user=request.user).exists():
                return self.doctor_status
            if Director.objects.filter(user=request.user).exists():
                return self.director_status
        return self.return_status

    
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

        
class VisitPermissions(BasePermission):

    P_METHODS = ('GET', 'HEAD', 'OPTIONS', 'PUT','PATH','POST')
    D_METHODS = ('GET', 'HEAD', 'OPTIONS', 'PUT','PATH',)
    C_METHODS = ('GET', 'HEAD', 'OPTIONS', 'PUT','PATH','POST','DELETE')
    NOT_ALLOWED= ('PUT','PATH','POST','DELETE')

    def has_permission(self, request,view):
        if request.user.is_authenticated:
            if request.user.usertype =='p':
                return bool(request.method in self.C_METHODS)
            if request.user.usertype =='d':
                return bool(request.method in self.P_METHODS)
            if request.user.usertype =='c':
                return bool(request.method in self.P_METHODS)
        else:
            return False
            
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.user.usertype =='p':
                if obj.closed == True and request.method in SAFE_METHODS:
                    return True
                if obj.closed == False and request.method in self.NOT_ALLOWED:
                    return False
            if request.user.usertype =='d':
                if obj.closed == True and request.method in SAFE_METHODS:
                    return True
                if obj.closed == False and request.method in self.NOT_ALLOWED:
                    return False
            if request.user.usertype =='c':
                if request.method in self.D_METHODS:
                    return True
            else:
                False
        else:
            False
                
            
            
    