from rest_framework import viewsets
from teams.models.viewer import Viewer
from teams.serializers.viewer import AdminViewerSerializer, ProjectViewerSerializer
from config.permissions import AdminOnly
from rest_framework.permissions import IsAuthenticated


class ViewerModelView(viewsets.ModelViewSet):
    queryset = Viewer.objects.all()
    serializer_class = AdminViewerSerializer
    permission_classes = [IsAuthenticated, AdminOnly]
    
    def get_serializer_class(self):
        if 'project_pk' in self.kwargs:
            return ProjectViewerSerializer
        return super().get_serializer_class()
    
    def get_queryset(self):
        if 'project_pk' in self.kwargs:
            return Viewer.objects.filter(project__pk=self.kwargs['project_pk']).all().order_by('-id')

        return Viewer.objects.all().order_by('-id')
    
    def perform_create(self, serializer):
        if 'project_pk' in self.kwargs:
            serializer.save(project = self.kwargs['project_pk'])
        else:
            serializer.save()

    
