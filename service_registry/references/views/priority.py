from rest_framework import viewsets
from references.models.priority import Priority
from references.serializers.priority import PriorityChoicesSerializer, PrioritySerializer
from config.permissions import AdminOnly
from rest_framework.permissions import IsAuthenticated

class PriorityChoicesModelView(viewsets.ReadOnlyModelViewSet):
    queryset = Priority.objects.all().order_by('-id')
    serializer_class = PriorityChoicesSerializer

class PriorityModelView(viewsets.ModelViewSet):
    queryset = Priority.objects.all().order_by('-id')
    serializer_class = PrioritySerializer
    permission_classes = [IsAuthenticated, AdminOnly]
    pagination_class = None 