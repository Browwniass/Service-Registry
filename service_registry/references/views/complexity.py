from rest_framework import viewsets
from references.models.complexity import Complexity
from references.serializers.complexity import ComplexityChoicesSerializer, ComplexitySerializer
from config.permissions import AdminOnly
from rest_framework.permissions import IsAuthenticated


class ComplexityChoicesModelView(viewsets.ReadOnlyModelViewSet):
    queryset = Complexity.objects.all()
    serializer_class = ComplexityChoicesSerializer
    
class ComplexityModelView(viewsets.ModelViewSet):
    queryset = Complexity.objects.all()
    serializer_class = ComplexitySerializer  
    permission_classes = [IsAuthenticated, AdminOnly]