from rest_framework import viewsets
from comments.models import Comment
from comments.serializers import CommentListSerializer, CommentDetailSerializer
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from teams.models.user import User
from config.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class CommentModelView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    
    def get_serializer_class(self):
        user = self.request.user
        if not(user.is_anonymous) and user.role == User.ROLE_CHOICES[0][0]:
            return CommentDetailSerializer
        return super().get_serializer_class()
    
    def get_queryset(self):
        if 'project_pk' in self.kwargs:
            user = self.request.user
            if not(user.is_anonymous) and user.role == User.ROLE_CHOICES[0][0]:
                return Comment.objects.filter(project=self.kwargs['project_pk'])
            return Comment.objects.filter(project=self.kwargs['project_pk'], is_hidden=False)
        
        if 'layer_pk' in self.kwargs:
            return Comment.objects.filter(layer=self.kwargs['layer_pk'])
        
        #Hiding a "deleted" comment
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_hidden = True
        instance.date_delete = timezone.localtime(timezone.now())
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)  # Ответ, указывающий на успешное удаление