from rest_framework import permissions
from teams.models.user import User
from teams.models.member import Member
from teams.models.stackholder import Stackholder


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated  and request.user.role == User.ROLE_CHOICES[0][0])

class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return False

class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated  and request.user.role == User.ROLE_CHOICES[0][0])
    
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        is_member = Member.objects.filter(project=obj.project, worker__user=request.user).exists()
        is_stackholder = Stackholder.objects.filter(project=obj.project, viewer__user=request.user).exists()
        # Instance must have an attribute named `user`.
        return (request.user.role == User.ROLE_CHOICES[0][0]) or ((is_member or is_stackholder) and (obj.created == request.user))
    
class IsMemberOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        print(obj.project)
        is_member = Member.objects.filter(project=obj.project, worker__user=request.user).exists()
        
        # Instance must have an attribute named `user`.
        return (request.user.role == User.ROLE_CHOICES[0][0]) or is_member