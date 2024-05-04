from rest_framework import viewsets
from teams.models.stackholder import Stackholder
from teams.serializers.stackholder import StackholderSerializer
from config.permissions import IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class StackholderModelView(viewsets.ModelViewSet):
    queryset = Stackholder.objects.all()
    serializer_class = StackholderSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    
    def get_queryset(self):
        if 'project_pk' in self.kwargs:
            return Stackholder.objects.filter(project=self.kwargs['project_pk'])
    