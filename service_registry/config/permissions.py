from rest_framework import permissions
from teams.models.user import User
from teams.models.member import Member
from teams.models.stackholder import Stackholder
from projects.models.project import Project
from teams.models.viewer import Viewer
from teams.models.worker import Worker


class IsRoleOwnRoot(permissions.BasePermission):
    def has_permission(self, request, view):
        url_list = (request.path).split('/')
        is_admin_url = 'adminn' in url_list
        is_viewer_url = 'viewer' in url_list
        is_member_url = 'member' in url_list

        is_admin = request.user.is_admin == True and is_admin_url
        is_member = Worker.objects.filter(user=request.user).exists() and is_member_url
        #is_member =  (member.first().is_archived == False) and member.exists() and is_member_url
        is_viewer = Viewer.objects.filter(user=request.user).exists() and is_viewer_url
        #print(view.serializer_class.Meta.model.__name__)
        #print(view.que)
        #allowed_viewer = Viewer.objects.filter(project__id=project_id, worker__user=request.user).exists()
        return (is_viewer or is_admin or is_member) 
        #return (is_viewer or is_member or is_admin)
    

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Only Admin allowed to mutations
    """
    def has_permission(self, request, view):
        url_list = (request.path).split('/')
        is_admin_url = 'adminn' in url_list

        if request.method in permissions.SAFE_METHODS:
            return True

        return is_admin_url
    

class ReadOnly(permissions.BasePermission):
    """
    All roles only allowed to Read
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return False


class AdminOnly(permissions.BasePermission):
    """
    Only Admin allowed to do anything
    """
    def has_permission(self, request, view):
        url_list = (request.path).split('/')
        is_admin_url = 'adminn' in url_list
        
        return is_admin_url


class ViewerIsAllowed(permissions.BasePermission):
    """
    Determines whether this viewer has the permission to be on this resource.
    Nedeed for nested relations
    """
    def has_permission(self, request, view):
        url_list = (request.path).split('/')
        is_viewer_url = 'viewer' in url_list
        
        # If viewer, then check if user is allowed to project
        if is_viewer_url:
            if 'projects' in url_list:
                project_id = url_list[url_list.index('projects')+1]
            # In case url through layers
            elif 'layers' in url_list:
                project_id = Project.objects.get(layer__id=url_list[url_list.index('layers')+1]).pk
            
            viewer = Viewer.objects.filter(user=request.user).prefetch_related('project').first()
            # Сhecking whether this user is associated with the requested project
            is_viewer_on_project = int(project_id) in list(viewer.project.values_list('id', flat=True))
            
            return viewer.is_full or is_viewer_on_project
        # Other roles can freely get this resources
        else: 
            return True
    


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission to allow only admin, members of project or projects stackeholders create new comments and read them
    """
    def has_permission(self, request, view):
        url_list = (request.path).split('/')
        is_viewer_url = 'viewer' in url_list
        
        if 'projects' in url_list: 
            project_id = url_list[url_list.index('projects')+1]
        if 'layers' in url_list: 
            project_id = Project.objects.filter(layer__id=url_list[url_list.index('layers')+1]).first().pk

        is_stackholder = Stackholder.objects.filter(project__id=project_id, viewer__user=request.user).exists()

        if request.method in permissions.SAFE_METHODS:
            # Viewer can view comments only wnen he had stackholder instance
            if (is_viewer_url and not is_stackholder):
                return False
            return True
        
        # Сhecking whether this member is associated with the requested project
        is_member = Member.objects.filter(project__id=project_id, is_approved=True, worker__user=request.user).exists()
        is_admin_url = 'adminn' in url_list
        is_member_url = 'member' in url_list

        return is_admin_url or ((is_member and is_member_url) or (is_stackholder and is_viewer_url))

    def has_object_permission(self, request, view, obj):
        """
        Object-Level Permission to allow only admin or owners of an comment to edit it.
        Only viewers with stackholder instance can edit.
        """
        # There is no need to register a stackholder separately, as it was clarified earlier
        if request.method in permissions.SAFE_METHODS:
            return True
        
        url_list = (request.path).split('/')
        is_admin_url = 'adminn' in url_list
        is_member_url = 'member' in url_list
        is_viewer_url = 'viewer' in url_list

        is_member = Member.objects.filter(project=obj.project, is_approved=True, worker__user=request.user).exists()
        is_stackholder = Stackholder.objects.filter(project=obj.project, viewer__user=request.user).exists()
        
        return is_admin_url or ((is_member and is_member_url) or (is_stackholder and is_viewer_url) and (obj.created == request.user))



class IsMemberOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission for Member object, that allow only for admin and worker create them.
    """
    def has_permission(self, request, view):
        url_list = (request.path).split('/') 

        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Worker can apply only through the project
        if 'projects' in url_list:
            is_member = Worker.objects.filter(user=request.user).exists()
        elif 'layers' in url_list:
            is_member = False

        is_admin_url = 'adminn' in url_list
        is_member_url = 'member' in url_list

        return is_admin_url or (is_member and is_member_url)

    def has_object_permission(self, request, view, obj):
        """
        Object-Level Permission for Member object, that allow only for admin and worker edit them.
        Workers can delete only their own application object instance
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        url_list = (request.path).split('/')
        is_admin_url = 'adminn' in url_list
        is_member_url = 'member' in url_list

        # Worker can edit only through the project
        if 'projects' in url_list:
            # Get worker application if it had not been seen by Admin
            is_member = Member.objects.filter(project=obj.project, worker__user=request.user, is_application=True, is_approved=None).exists()
        elif 'layers' in url_list:
            is_member = False

        # Member only allowed to delete his application when it not been seen by Admin
        if request.method == 'DELETE':
            return is_admin_url or ((is_member and is_member_url) and (obj.worker.user == request.user))
        
        return is_admin_url


class ReadOnlyForAssignedOrAdmin(permissions.BasePermission):
    """
    Permission for allowing only assigned on project members or stackholders view
    """
    def has_permission(self, request, view):
        url_list = (request.path).split('/') 
        is_admin_url = 'adminn' in url_list
        is_member_url = 'member' in url_list
        is_viewer_url = 'viewer' in url_list

        if 'projects' in url_list: 
            project_id = url_list[url_list.index('projects')+1]
        if 'layers' in url_list: 
            project_id = Project.objects.filter(layer__id=url_list[url_list.index('layers')+1]).first().pk

        is_member = Member.objects.filter(project=project_id, worker__user=request.user, is_approved=True).exists()
        is_viewer = Viewer.objects.filter(user=request.user, project=project_id).exists()

        if request.method in permissions.SAFE_METHODS:
            return is_admin_url or (is_member_url and is_member) or (is_viewer_url and is_viewer)

        return is_admin_url
