from rest_framework import viewsets
from projects.models.project import Project
from teams.models.viewer import Viewer
from teams.models.member import Member
from projects.serializers.project import ProjectSerializer, ProjectChoiceSerializer 
from config.permissions import IsAdminOrReadOnly, IsRoleOwnRoot
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied


class ProjectModelView(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsRoleOwnRoot, IsAdminOrReadOnly]

    def get_queryset(self):
        role = (self.request.path).split('/')
        is_viewer_url = 'viewer' in role
        is_member_url = 'member' in role
        if is_viewer_url:
            try:
                viewer = Viewer.objects.get(user=self.request.user)
            except Viewer.DoesNotExist:
                return []
        
            if viewer.is_full == False: # Если Наблюдатель не полный
                # Получаем только те проекты, что ему видимы
                return viewer.project.all().order_by('-id')
        if is_member_url: 
            if 'filt_member' in self.request.query_params:
                return Project.objects.filter(member__worker__user=self.request.user, member__is_approved=True).order_by('-id')
            elif 'filt_status' in self.request.query_params:
                return Project.objects.filter(status=self.request.query_params['filt_status']).order_by('-id')
        return Project.objects.all().order_by('-id') # Иначе все 

class ProjectChoiceModelView(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectChoiceSerializer
    pagination_class = None 
    permission_classes = [IsAuthenticated]
                          
    def get_queryset(self):
        params = self.request.query_params
        if 'viewer_pk' in params:
            try:
                viewer = Viewer.objects.get(pk=params['viewer_pk'])
            except Viewer.DoesNotExist:
                return []
            projects = viewer.project.all()
            return Project.objects.exclude(id__in=projects)
        return Project.objects.all().order_by('-id')

    
  