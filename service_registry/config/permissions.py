from rest_framework import permissions
from teams.models.user import User
from teams.models.member import Member
from teams.models.stackholder import Stackholder
from projects.models.project import Project
from teams.models.viewer import Viewer
from teams.models.worker import Worker

class IsRoleOwnRoot(permissions.BasePermission):
    def has_permission(self, request, view):
        role = (request.path).split('/')
        is_admin_url = 'adminn' in role
        is_viewer_url = 'viewer' in role
        is_member_url = 'member' in role

        is_admin = (request.user.role == User.ROLE_CHOICES[0][0] and is_admin_url)
        member = Worker.objects.filter(user=request.user)
        is_member =  (member.first().is_archived == False) and member.exists() and is_member_url
        is_viewer = Viewer.objects.filter(user=request.user).exists() and is_viewer_url
        #print(view.serializer_class.Meta.model.__name__)
        #print(view.que)
        #allowed_viewer = Viewer.objects.filter(project__id=project_id, worker__user=request.user).exists()
        return (is_viewer or is_member or is_admin)
    

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        role = (request.path).split('/')
        is_admin_url = 'adminn' in role

        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(request.user.role == User.ROLE_CHOICES[0][0] and is_admin_url)
    
class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return False

class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        role = (request.path).split('/')
        is_admin_url = 'adminn' in role
        #return bool(request.user and request.user.is_authenticated  and request.user.role == User.ROLE_CHOICES[0][0] and is_admin_url)
        return bool(request.user.role == User.ROLE_CHOICES[0][0] and is_admin_url)

class ViewerIsAllowed(permissions.BasePermission):
    def has_permission(self, request, view):
        url_list = (request.path).split('/')
        is_viewer_url = 'viewer' in url_list
        if is_viewer_url:
            if 'projects' in url_list:
                project_id = url_list[url_list.index('projects')+1]
            elif 'layers' in url_list:
                project_id = Project.objects.get(layer__id=url_list[url_list.index('layers')+1]).pk
            viewer = Viewer.objects.filter(user=request.user, project=project_id)
            return viewer.exists() and viewer.first().is_full == False
        else: return True
    

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    def has_permission(self, request, view):
        url_list = (request.path).split('/')
        is_viewer_url = 'viewer' in url_list
        if 'projects' in url_list: project_id = url_list[url_list.index('projects')+1]
        if 'layers' in url_list: project_id = Project.objects.get(layer__id=url_list[url_list.index('layers')+1]).pk
        is_stackholder = Stackholder.objects.filter(project__id=project_id, viewer__user=request.user).exists()

        if request.method in permissions.SAFE_METHODS or 'pk' in view.kwargs:
            if (is_viewer_url and not is_stackholder):
                return False
            return True
        
        is_member = Member.objects.filter(project__id=project_id, worker__user=request.user).exists()
        is_admin_url = 'adminn' in url_list
        is_member_url = 'member' in url_list
        return (request.user.role == User.ROLE_CHOICES[0][0] and is_admin_url) or (is_member and is_member_url or is_stackholder and is_viewer_url)

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        url_list = (request.path).split('/')
        is_admin_url = 'adminn' in url_list
        is_member_url = 'member' in url_list
        is_viewer_url = 'viewer' in url_list

        is_member = Member.objects.filter(project=obj.project, worker__user=request.user).exists()
        is_stackholder = Stackholder.objects.filter(project=obj.project, viewer__user=request.user).exists()
        # Instance must have an attribute named `user`.
        return (request.user.role == User.ROLE_CHOICES[0][0] and is_admin_url) or ((is_member and is_member_url or is_stackholder and is_viewer_url) and (obj.created == request.user))
        
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

        role = (request.path).split('/')
        is_admin_url = 'adminn' in role
        is_member_url = ['member'] in role

        # Instance must have an attribute named `user`.
        is_member = Member.objects.filter(project=obj.project, worker__user=request.user).exists()
        
        return (request.user.role == User.ROLE_CHOICES[0][0] and is_admin_url) or (is_member and is_member_url)