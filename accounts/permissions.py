from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import exceptions
from accounts.models import User


class IsProfileOwner(BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True
        
        logged_in_user = request.user
        if logged_in_user != obj.user:
            raise exceptions.PermissionDenied(
                "The logged_in_user is not Profile Owner")
        
        return True
