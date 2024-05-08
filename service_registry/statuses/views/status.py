from rest_framework import viewsets
from statuses.models.status import Status
from statuses.serializers.status import StatusChoicesSerializer, StatusSerializer
from config.permissions import AdminOnly


class StatusChoicesModelView(viewsets.ReadOnlyModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusChoicesSerializer

class StatusModelView(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [AdminOnly]