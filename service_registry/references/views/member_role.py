from rest_framework import viewsets
from references.models.member_role import MemberRole
from references.serializers.member_role import MemberRoleChoicesSerializer, MemberRoleSerializer
from config.permissions import AdminOnly
from rest_framework.permissions import IsAuthenticated


class MemberRoleChoicesModelView(viewsets.ReadOnlyModelViewSet):
    queryset = MemberRole.objects.all().order_by('-id')
    serializer_class = MemberRoleChoicesSerializer


class MemberRoleModelView(viewsets.ModelViewSet):
    queryset = MemberRole.objects.all().order_by('-id')
    serializer_class = MemberRoleSerializer
    permission_classes = [IsAuthenticated, AdminOnly]
    pagination_class = None 