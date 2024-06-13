from rest_framework import viewsets
from teams.models.member import Member
from teams.models.worker import Worker
from projects.models.project import Project
from teams.serializers.member import MemberListSerializer, MemberDetailSerializer
from config.permissions import IsMemberOwnerOrReadOnly, ViewerIsAllowed, IsRoleOwnRoot
from rest_framework.permissions import IsAuthenticated
from teams.models.user import User
from rest_framework import status
from rest_framework.response import Response


class MemberModelView(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberListSerializer
    permission_classes = [IsAuthenticated, IsRoleOwnRoot, ViewerIsAllowed, IsMemberOwnerOrReadOnly]

    def get_serializer_class(self):
        url_list = (self.request.path).split('/')
        is_admin_url = 'adminn' in url_list

        if is_admin_url:
            return MemberDetailSerializer
        
        return super().get_serializer_class()
    
    def get_queryset(self):
        if 'project_pk' in self.kwargs:
            return Member.objects.filter(project=self.kwargs['project_pk'])
        elif 'layer_pk' in self.kwargs:
            return Member.objects.filter(layer=self.kwargs['layer_pk'])
    
    def perform_create(self, serializer):
        url_list = (self.request.path).split('/')
        is_admin_url = 'adminn' in url_list
        # If not the admin, then the worker himself is assigned
        if not is_admin_url:
            worker = Worker.objects.get(user=self.request.user)
            if 'project_pk' in self.kwargs:
                serializer.save(project_id=self.kwargs['project_pk'], worker=worker, is_application=True)
            elif 'layer_pk' in self.kwargs:
                #serializer.save(layer_id=self.kwargs['layer_pk'], worker=worker)
                # Only Admin can put an employee on the layer
                return Response(status.HTTP_401_UNAUTHORIZED)
        # Аdmin can choose which employee to attach 
        elif 'project_pk' in self.kwargs:
            serializer.save(project_id=self.kwargs['project_pk'])
        elif 'layer_pk' in self.kwargs:
            serializer.save(layer_id=self.kwargs['layer_pk'])
        
    def perform_destroy(self, instance):
        # When deleting an object of Member, cascade deletion of all objects of these members inside the project layers
        if 'project_pk' in self.kwargs:
            layer_members = Member.objects.filter(layer__project=instance.project, worker=instance.worker)
            
            for member in layer_members:
                member.delete()

        return super().perform_destroy(instance)

        
    