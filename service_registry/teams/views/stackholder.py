from rest_framework import viewsets
from teams.models.stackholder import Stackholder
from teams.serializers.stackholder import StackholderSerializer
from config.permissions import IsAdminOrReadOnly, ViewerIsAllowed, IsRoleOwnRoot
from rest_framework.permissions import IsAuthenticated

class StackholderModelView(viewsets.ModelViewSet):
    queryset = Stackholder.objects.all()
    serializer_class = StackholderSerializer
    permission_classes = [IsAuthenticated, IsRoleOwnRoot, ViewerIsAllowed, IsAdminOrReadOnly]
    
    def get_queryset(self):
        if 'project_pk' in self.kwargs:
            return Stackholder.objects.filter(project=self.kwargs['project_pk']).order_by('-id')
    
    def perform_create(self, serializer):
        if 'project_pk' in self.kwargs:
            serializer.save(project_id = self.kwargs['project_pk'])