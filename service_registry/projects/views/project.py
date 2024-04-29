from rest_framework import viewsets

from projects.models.project import Project
from projects.serializers.project import ProjectSerializer 


class ProjectModelView(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    
  