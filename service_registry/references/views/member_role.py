from rest_framework import viewsets
from references.models.member_role import MemberRole
from references.serializers.member_role import MemberRoleChoicesSerializer 


class MemberRoleChoicesModelView(viewsets.ReadOnlyModelViewSet):
    queryset = MemberRole.objects.all()
    serializer_class = MemberRoleChoicesSerializer
    