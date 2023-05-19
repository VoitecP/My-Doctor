from rest_framework import permissions
from apps.core.models import Patient, User, Doctor

class IsNotUserUpdated(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if Patient.objects.filter(user=request.user).exists():
                return False
            if Doctor.objects.filter(user=request.user).exists():
                return False
        return True

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request so we'll always
        # allow GET, HEAD, or OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True

        # # Write permissions are only allowed to the user
        return obj.user == request.user



class IsUserUpdated(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if Patient.objects.filter(user=request.user).exists():
                return True
            if Doctor.objects.filter(user=request.user).exists():
                return True
        return False

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request so we'll always
        # allow GET, HEAD, or OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True

        # # Write permissions are only allowed to the user
        return obj.user == request.user


class IsPatient(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.usertype == 'p':
                return True
        return False

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request so we'll always
        # allow GET, HEAD, or OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True

        # # Write permissions are only allowed to the user
        return obj.user == request.user


class IsDoctor(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.usertype == 'd':
                return True
        return False

    def has_object_permission(self, request, view, obj):
    # Read permissions are allowed to any request so we'll always
    # allow GET, HEAD, or OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True

    # # Write permissions are only allowed to the user
        return obj.user == request.user


class IsPatientCreated(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if Patient.objects.filter(user=request.user).exists():
                return True
        return False

    def has_object_permission(self, request, view, obj):
    # Read permissions are allowed to any request so we'll always
    # allow GET, HEAD, or OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True

    # # Write permissions are only allowed to the user
        return obj.user == request.user

class IsDoctorCreated(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if Doctor.objects.filter(user=request.user).exists():  #  == True:
                return True
        return False

    def has_object_permission(self, request, view, obj):
    # Read permissions are allowed to any request so we'll always
    # allow GET, HEAD, or OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True

    # # Write permissions are only allowed to the user
        return obj.user == request.user