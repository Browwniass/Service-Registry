from rest_framework import viewsets
from references.models.project_type import ProjectType
from references.serializers.project_type import ProjectTypeChoicesSerializer 


class ProjectTypeChoicesModelView(viewsets.ReadOnlyModelViewSet):
    queryset = ProjectType.objects.all()
    serializer_class = ProjectTypeChoicesSerializer
    