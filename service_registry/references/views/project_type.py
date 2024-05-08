from rest_framework import viewsets
from references.models.project_type import ProjectType
from references.serializers.project_type import ProjectTypeChoicesSerializer, ProjectTypeSerializer
from config.permissions import AdminOnly


class ProjectTypeChoicesModelView(viewsets.ReadOnlyModelViewSet):
    queryset = ProjectType.objects.all()
    serializer_class = ProjectTypeChoicesSerializer

class ProjectTypeModelView(viewsets.ModelViewSet):
    queryset = ProjectType.objects.all()
    serializer_class = ProjectTypeSerializer
    permission_classes = [AdminOnly]
    