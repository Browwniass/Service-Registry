from rest_framework import viewsets
from projects.models.stack import Stack, StackElement
from projects.serializers.stack import StackChoicesSerializer, StackSerializer, StackElementSerializer
from config.permissions import AdminOnly


class StackElementModelView(viewsets.ModelViewSet):
    queryset = StackElement.objects.all()
    serializer_class = StackElementSerializer
    permission_classes = [AdminOnly]

class StackModelView(viewsets.ModelViewSet):
    queryset = Stack.objects.all()
    serializer_class = StackSerializer
    permission_classes = [AdminOnly]

class StackChoicesModelView(viewsets.ReadOnlyModelViewSet):
    queryset = Stack.objects.all()
    serializer_class = StackChoicesSerializer
