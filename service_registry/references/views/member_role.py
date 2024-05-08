from rest_framework import viewsets
from references.models.member_role import MemberRole
from references.serializers.member_role import MemberRoleChoicesSerializer, MemberRoleSerializer
from config.permissions import AdminOnly


class MemberRoleChoicesModelView(viewsets.ReadOnlyModelViewSet):
    queryset = MemberRole.objects.all()
    serializer_class = MemberRoleChoicesSerializer

class MemberRoleModelView(viewsets.ModelViewSet):
    queryset = MemberRole.objects.all()
    serializer_class = MemberRoleSerializer
    permission_classes = [AdminOnly]