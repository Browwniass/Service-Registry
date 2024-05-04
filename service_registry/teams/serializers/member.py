from rest_framework import serializers
from teams.models.member import Member
from projects.models.layer import Layer
from projects.serializers.layer import LayerSerializer
from teams.models.worker import Worker
from teams.serializers.worker import WorkerListSerializer
from references.models.member_role import MemberRole
from references.serializers.member_role import MemberRoleSerializer

#List Serializer of the Member model
class MemberListSerializer(serializers.ModelSerializer):
    layer_id = serializers.PrimaryKeyRelatedField(queryset=Layer.objects.all(), source='layer', write_only=True)
    layer = LayerSerializer(read_only=True)
    worker_id = serializers.PrimaryKeyRelatedField(queryset=Worker.objects.all(), source='worker', write_only=True)
    worker = WorkerListSerializer(read_only=True)
    role_id = serializers.PrimaryKeyRelatedField(queryset=MemberRole.objects.all(), source='role', write_only=True)
    role = MemberRoleSerializer(read_only=True)
    class Meta:
        model = Member
        fields = ['id', 'role', 'role_id', 'project', 'layer', 'layer_id', 'worker', 'worker_id', 'date_joining', 'date_termination']

#Detail Serializer of the Member model
class MemberDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = "__all__"