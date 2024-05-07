from rest_framework import viewsets
from statuses.models.status import Status
from statuses.serializers.status import StatusChoicesSerializer 


class StatusChoicesModelView(viewsets.ReadOnlyModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusChoicesSerializer
    