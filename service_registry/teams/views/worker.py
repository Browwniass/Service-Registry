from rest_framework import viewsets
from teams.serializers.worker import WorkerDetailSerializer
from teams.models.worker import Worker
from config.permissions import ReadOnly, AdminOnly
from rest_framework.permissions import IsAuthenticated


class WorkerModelView(viewsets.ModelViewSet):
    queryset = Worker.objects.all().order_by('-id')
    serializer_class = WorkerDetailSerializer
    permission_classes = [IsAuthenticated, AdminOnly]

    