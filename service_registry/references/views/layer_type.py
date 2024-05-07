from rest_framework import viewsets

from references.models.layer_type import LayerType
from references.serializers.layer_type import LayerTypeChoicesSerializer 


class LayerTypeChoicesModelView(viewsets.ReadOnlyModelViewSet):
    queryset = LayerType.objects.all()
    serializer_class = LayerTypeChoicesSerializer
    
  