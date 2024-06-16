from rest_framework import viewsets
from projects.models.layer import Layer
from projects.models.project import Project
from teams.models.viewer import Viewer
from projects.serializers.layer import LayerSerializer 
from config.permissions import IsAdminOrReadOnly, ViewerIsAllowed, IsRoleOwnRoot
from rest_framework.permissions import IsAuthenticated

class LayerModelView(viewsets.ModelViewSet):
    queryset = Layer.objects.all()
    serializer_class = LayerSerializer
    permission_classes = [IsAuthenticated, IsRoleOwnRoot, IsAdminOrReadOnly, ViewerIsAllowed]
    
    def get_queryset(self):
        if 'project_pk' in self.kwargs:
            return Layer.objects.filter(project=self.kwargs['project_pk']).order_by('-id')
        else:
            role = (self.request.path).split('/')
            is_viewer_url = 'viewer' in role
            if is_viewer_url:
                try:
                    viewer = Viewer.objects.prefetch_related('project').get(user=self.request.user)
                except Viewer.DoesNotExist:
                    return []
                if not(viewer.is_full):
                    projects = viewer.project.all()
                    return Layer.objects.filter(project__in=projects).order_by('-id')
            return Layer.objects.all().order_by('-id')
    
    def perform_create(self, serializer):
        if 'project_pk' in self.kwargs:
            serializer.save(project_id = self.kwargs['project_pk'] )
"""        if 'layer_pk' in self.kwargs:
            project = Project.objects.get(layer__id=self.kwargs['layer_pk'])
            serializer.save(created_id=self.request.user.pk, layer_id = self.kwargs['layer_pk'], project_id=project.pk)"""
        