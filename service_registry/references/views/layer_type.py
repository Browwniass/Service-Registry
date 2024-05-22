from rest_framework import viewsets
from references.models.layer_type import LayerType
from references.serializers.layer_type import LayerTypeChoicesSerializer, LayerTypeSerializer
from config.permissions import AdminOnly
from rest_framework.permissions import IsAuthenticated


class LayerTypeChoicesModelView(viewsets.ReadOnlyModelViewSet):
    queryset = LayerType.objects.all()
    serializer_class = LayerTypeChoicesSerializer
    
class LayerTypeModelView(viewsets.ModelViewSet):
    queryset = LayerType.objects.all()
    serializer_class = LayerTypeSerializer
    permission_classes = [IsAuthenticated, AdminOnly]  