from rest_framework import viewsets
from statuses.models.status import Status
from statuses.serializers.status import StatusChoicesSerializer, StatusSerializer
from config.permissions import AdminOnly
from rest_framework.permissions import IsAuthenticated


class StatusChoicesModelView(viewsets.ReadOnlyModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusChoicesSerializer
    pagination_class = None 
    permission_classes = [IsAuthenticated]

class StatusModelView(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [IsAuthenticated, AdminOnly]
    pagination_class = None 