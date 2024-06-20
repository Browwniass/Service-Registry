from rest_framework import viewsets
from projects.models.document import ProjectDocument
from rest_framework.parsers import MultiPartParser, FormParser
from projects.serializers.document import ProjectDocumentListSerializer, ProjectDocumentDetailSerializer 
from projects.models.project import Project 
from config.permissions import IsAdminOrReadOnly, ViewerIsAllowed, ReadOnlyForAssignedOrAdmin, IsRoleOwnRoot
from rest_framework.permissions import IsAuthenticated
from teams.models.user import User
from teams.models.member import Member

class ProjectDocumentModelView(viewsets.ModelViewSet):
    queryset = ProjectDocument.objects.all()
    serializer_class = ProjectDocumentListSerializer
    permission_classes = [IsAuthenticated, IsRoleOwnRoot, ViewerIsAllowed, ReadOnlyForAssignedOrAdmin]
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_class(self):
        user = self.request.user
        role = (self.request.path).split('/')
        is_admin_url = 'adminn' in role
        
        if not(user.is_anonymous) and user.is_admin and is_admin_url:
            return ProjectDocumentDetailSerializer
        
        return super().get_serializer_class()
    
    def get_queryset(self):
        if 'project_pk' in self.kwargs:
            return ProjectDocument.objects.filter(project=self.kwargs['project_pk'])
        
        return ProjectDocument.objects.all().order_by('-id')
    
    def perform_create(self, serializer):
        if 'project_pk' in self.kwargs:
            serializer.save(project_id = self.kwargs['project_pk']).order_by('-id')
