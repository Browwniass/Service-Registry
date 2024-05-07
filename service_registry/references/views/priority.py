from rest_framework import viewsets
from references.models.priority import Priority
from references.serializers.priority import PriorityChoicesSerializer 


class PriorityChoicesModelView(viewsets.ReadOnlyModelViewSet):
    queryset = Priority.objects.all()
    serializer_class = PriorityChoicesSerializer
    