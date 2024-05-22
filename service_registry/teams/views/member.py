from rest_framework import viewsets
from teams.models.member import Member
from projects.models.project import Project
from teams.serializers.member import MemberListSerializer, MemberDetailSerializer
from config.permissions import IsAdminOrReadOnly, ViewerIsAllowed, IsRoleOwnRoot
from rest_framework.permissions import IsAuthenticated
from teams.models.user import User


class MemberModelView(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberListSerializer
    permission_classes = [IsAuthenticated, IsRoleOwnRoot, ViewerIsAllowed, IsAdminOrReadOnly]

    def get_serializer_class(self):
        user = self.request.user
        role = (self.request.path).split('/')
        is_admin_url = 'adminn' in role

        if user.role == User.ROLE_CHOICES[0][0] and is_admin_url:
            return MemberDetailSerializer
        return super().get_serializer_class()
    
    def get_queryset(self):
        if 'project_pk' in self.kwargs:
            return Member.objects.filter(project=self.kwargs['project_pk'])
        if 'layer_pk' in self.kwargs:
            return Member.objects.filter(layer=self.kwargs['layer_pk'])
    
    def perform_create(self, serializer):
        if 'project_pk' in self.kwargs:
            serializer.save(project_id = self.kwargs['project_pk'] )
        if 'layer_pk' in self.kwargs:
            project = Project.objects.get(layer__id=self.kwargs['layer_pk'])
            serializer.save(layer_id = self.kwargs['layer_pk'], project_id=project.pk)
        
    