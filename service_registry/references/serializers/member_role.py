from rest_framework import serializers
from references.models.member_role import MemberRole

class MemberRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberRole 
        fields = "__all__"
    