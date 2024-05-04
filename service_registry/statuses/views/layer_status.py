from rest_framework import viewsets
from statuses.models.layer_status import ChangeLayerStatus
from statuses.serializers.layer_status import ChangeLayerStatusSerializer 
from config.permissions import ReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class ChangeLayerStatusModelView(viewsets.ModelViewSet):
    queryset = ChangeLayerStatus.objects.all()
    serializer_class = ChangeLayerStatusSerializer
    permission_classes = [ReadOnly]

    def get_queryset(self):
        if 'layer_pk' in self.kwargs:
            return ChangeLayerStatus.objects.filter(layer=self.kwargs['layer_pk'])