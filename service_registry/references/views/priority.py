from rest_framework import viewsets
from references.models.priority import Priority
from references.serializers.priority import PriorityChoicesSerializer, PrioritySerializer
from config.permissions import AdminOnly

class PriorityChoicesModelView(viewsets.ReadOnlyModelViewSet):
    queryset = Priority.objects.all()
    serializer_class = PriorityChoicesSerializer

class PriorityModelView(viewsets.ModelViewSet):
    queryset = Priority.objects.all()
    serializer_class = PrioritySerializer
    permission_classes = [AdminOnly]