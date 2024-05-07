from rest_framework import serializers
from references.models.member_role import MemberRole

class MemberRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberRole 
        fields = "__all__"

class MemberRoleChoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberRole 
        fields = "__all__"
        read_only_fields = ('name', 'description', 'color')
    