from rest_framework import viewsets
from teams.models.member import Member
from teams.serializers.member import MemberListSerializer
from config.permissions import IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class MemberModelView(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]

    def get_queryset(self):
        if 'project_pk' in self.kwargs:
            return Member.objects.filter(project=self.kwargs['project_pk'])
        if 'layer_pk' in self.kwargs:
            return Member.objects.filter(layer=self.kwargs['layer_pk'])
        
    