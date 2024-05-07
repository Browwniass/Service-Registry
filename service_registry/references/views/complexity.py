from rest_framework import viewsets

from references.models.complexity import Complexity
from references.serializers.complexity import ComplexityChoicesSerializer 


class ComplexityChoicesModelView(viewsets.ReadOnlyModelViewSet):
    queryset = Complexity.objects.all()
    serializer_class = ComplexityChoicesSerializer
    
  