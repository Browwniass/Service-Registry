from rest_framework import viewsets
from projects.models.layer import Layer
from projects.serializers.layer import LayerSerializer 


class LayerModelView(viewsets.ModelViewSet):
    queryset = Layer.objects.all()
    serializer_class = LayerSerializer
    
    def get_queryset(self):
        if 'project_pk' in self.kwargs:
            return Layer.objects.filter(project=self.kwargs['project_pk'])
        
        return Layer.objects.all()
    