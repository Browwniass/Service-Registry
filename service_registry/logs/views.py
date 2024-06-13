from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from logs.models import HistoryOfChange
from logs.serializers import HistoryOfChangeSerializer
from projects.models.project import Project
from projects.models.layer import Layer
from config.permissions import ReadOnly, AdminOnly, ViewerIsAllowed
from rest_framework.permissions import IsAuthenticated


class NestedHistoryOfChangeModelView(viewsets.ReadOnlyModelViewSet):
    queryset = HistoryOfChange.objects.all()
    serializer_class = HistoryOfChangeSerializer
    permission_classes = [IsAuthenticated, ReadOnly, ViewerIsAllowed]
    

    def get_queryset(self):
        if 'project_pk' in self.kwargs:
            project_pk = self.kwargs.get('project_pk')
            project = get_object_or_404(Project, pk=project_pk)
            return project.history.all()
        if 'layer_pk' in self.kwargs:
            layer_pk = self.kwargs.get('layer_pk')
            layer = get_object_or_404(Layer, pk=layer_pk)
            return layer.history.all()

class FullHistoryOfChangeModelView(viewsets.ReadOnlyModelViewSet):
    queryset = HistoryOfChange.objects.all()
    serializer_class = HistoryOfChangeSerializer
    permission_classes = [IsAuthenticated, AdminOnly]
    