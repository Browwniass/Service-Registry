from rest_framework import viewsets
from projects.models.document import ProjectDocument
from projects.serializers.document import ProjectDocumentListSerializer, ProjectDocumentDetailSerializer 
from config.permissions import IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from teams.models.user import User
from teams.models.member import Member

class ProjectDocumentModelView(viewsets.ModelViewSet):
    queryset = ProjectDocument.objects.all()
    serializer_class = ProjectDocumentListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]

    def get_serializer_class(self):
        user = self.request.user
        if not(user.is_anonymous) and user.role == User.ROLE_CHOICES[0][0]:
            return ProjectDocumentDetailSerializer
        return super().get_serializer_class()
    
    def get_queryset(self):
        if 'project_pk' in self.kwargs:
            return ProjectDocument.objects.filter(project=self.kwargs['project_pk'])