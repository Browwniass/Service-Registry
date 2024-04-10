from rest_framework import permissions
from django.contrib.auth.models import Permission
from .models import User


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated  and request.user.role == User.ROLE_CHOICES[0][0])

class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated  and request.user.role == User.ROLE_CHOICES[0][0])
    
