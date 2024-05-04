from rest_framework import viewsets
from statuses.models.project_status import ChangeProjectStatus
from statuses.serializers.project_status import ChangeProjectStatusSerializer 
from config.permissions import ReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class ChangeProjectStatusModelView(viewsets.ModelViewSet):
    queryset = ChangeProjectStatus.objects.all()
    serializer_class = ChangeProjectStatusSerializer
    permission_classes = [ReadOnly]

    def get_queryset(self):
        if 'project_pk' in self.kwargs:
            return ChangeProjectStatus.objects.filter(project=self.kwargs['project_pk'])
    