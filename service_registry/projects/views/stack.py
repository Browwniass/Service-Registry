from rest_framework import viewsets
from projects.models.stack import Stack
from projects.serializers.stack import StackChoicesSerializer 


class StackChoicesModelView(viewsets.ReadOnlyModelViewSet):
    queryset = Stack.objects.all()
    serializer_class = StackChoicesSerializer