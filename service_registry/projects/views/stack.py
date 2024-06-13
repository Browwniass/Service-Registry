from rest_framework import viewsets
from projects.models.stack import Stack, StackElement
from projects.serializers.stack import StackChoicesSerializer, StackElementChoicesSerializer, StackSerializer, StackElementSerializer
from config.permissions import AdminOnly
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated


class StackElementModelView(viewsets.ModelViewSet):
    queryset = StackElement.objects.all()
    serializer_class = StackElementSerializer
    permission_classes = [IsAuthenticated, AdminOnly]

    def get_queryset(self):
        if 'stack_pk' in self.kwargs:
            try:
                stack = Stack.objects.get(pk=self.kwargs['stack_pk'])
            except Stack.DoesNotExist:
                return []
            return stack.elements.all()
        return StackElement.objects.all()
    

    def perform_create(self, serializer):    
        if 'stack_pk' in self.kwargs:
            stack = Stack.objects.get(pk=self.kwargs['stack_pk'])
            new_element = serializer.save()
            stack.elements.add(new_element)
            #print(ints.elements.all())
        else:
            serializer.save()
    
        
class StackModelView(viewsets.ModelViewSet):
    queryset = Stack.objects.all()
    serializer_class = StackSerializer
    permission_classes = [IsAuthenticated, AdminOnly]

class StackChoicesModelView(viewsets.ReadOnlyModelViewSet):
    queryset = Stack.objects.all()
    serializer_class = StackChoicesSerializer

class StackElementChoicesModelView(viewsets.ReadOnlyModelViewSet):
    queryset = StackElement.objects.all()
    serializer_class = StackElementChoicesSerializer

    def get_queryset(self):
        params = self.request.query_params
        if 'stack_pk' in params:
            try:
                stack = Stack.objects.get(pk=params['stack_pk'])
            except Stack.DoesNotExist:
                return []
            elements = stack.elements.all()
            return StackElement.objects.exclude(id__in=elements)
        return StackElement.objects.all()
