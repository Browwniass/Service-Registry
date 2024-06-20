from rest_framework import viewsets
from comments.models import Comment
from comments.serializers import CommentListSerializer, CommentDetailSerializer
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from teams.models.user import User
from projects.models.project import Project
from config.permissions import IsOwnerOrReadOnly, ViewerIsAllowed, IsRoleOwnRoot
from rest_framework.permissions import IsAuthenticated


class CommentModelView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentListSerializer
    permission_classes = [IsAuthenticated, IsRoleOwnRoot, ViewerIsAllowed, IsOwnerOrReadOnly]


    def get_serializer_class(self):
        user = self.request.user
        role = (self.request.path).split('/')
        is_admin_url = 'adminn' in role

        if not(user.is_anonymous) and user.is_admin and is_admin_url:
            return CommentDetailSerializer
        return super().get_serializer_class()
    
    def get_queryset(self):
        if 'project_pk' in self.kwargs:
            user = self.request.user
            if not(user.is_anonymous) and user.is_admin:
                return Comment.objects.filter(project=self.kwargs['project_pk']).order_by('id')
            return Comment.objects.filter(project=self.kwargs['project_pk'], is_hidden=False).order_by('id')
        
        if 'layer_pk' in self.kwargs:
            user = self.request.user
            if not(user.is_anonymous) and user.is_admin:
                 return Comment.objects.filter(layer=self.kwargs['layer_pk']).order_by('id')
            return Comment.objects.filter(layer=self.kwargs['layer_pk'], is_hidden=False).order_by('id')
    
        if 'document_pk' in self.kwargs:
            user = self.request.user
            if not(user.is_anonymous) and user.is_admin:
                 return Comment.objects.filter(document=self.kwargs['document_pk']).order_by('id')
            return Comment.objects.filter(document__id=self.kwargs['document_pk'], is_hidden=False).order_by('id')
    
    def perform_create(self, serializer):
        if 'project_pk' in self.kwargs:
            serializer.save(created_id=self.request.user.pk, project_id = self.kwargs['project_pk'])
        if 'layer_pk' in self.kwargs:
            project = Project.objects.get(layer__id=self.kwargs['layer_pk'])
            serializer.save(created_id=self.request.user.pk, layer_id = self.kwargs['layer_pk'], project_id=project.pk)
        if 'document_pk' in self.kwargs:
            project = Project.objects.get(projectdocument__id=self.kwargs['document_pk'])
            serializer.save(created_id=self.request.user.pk, document_id = self.kwargs['document_pk'], project_id=project.pk)
    #Hiding a "deleted" comment
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_hidden = True
        instance.date_delete = timezone.localtime(timezone.now())
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)  # Ответ, указывающий на успешное удаление