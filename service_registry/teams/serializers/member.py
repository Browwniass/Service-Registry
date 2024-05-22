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
    worker_id = serializers.PrimaryKeyRelatedField(queryset=Worker.objects.all(), source='worker', write_only=True)
    worker = WorkerListSerializer(read_only=True)
    role_id = serializers.PrimaryKeyRelatedField(queryset=MemberRole.objects.all(), source='role', write_only=True)
    role = MemberRoleSerializer(read_only=True)
    
    class Meta:
        model = Member
        fields = ['id', 'role', 'role_id', 'project', 'layer', 'worker', 'worker_id', 'date_joining', 'date_termination']
        read_only_fields = ['project', 'layer']
        
#Detail Serializer of the Member model
class MemberDetailSerializer(serializers.ModelSerializer):
    worker_id = serializers.PrimaryKeyRelatedField(queryset=Worker.objects.all(), source='worker', write_only=True)
    worker = WorkerListSerializer(read_only=True)
    role_id = serializers.PrimaryKeyRelatedField(queryset=MemberRole.objects.all(), source='role', write_only=True)
    role = MemberRoleSerializer(read_only=True)

    class Meta:
        model = Member
        fields = "__all__"
        read_only_fields = ['project', 'layer']