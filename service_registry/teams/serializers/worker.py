from rest_framework import serializers
from teams.models.worker import Worker
from teams.models.user import User
from teams.serializers.user import UserSerializer
from projects.models.stack import Stack
from projects.serializers.stack import StackSerializer

#List Serializer of the Worker model
class WorkerListSerializer(serializers.ModelSerializer):
    
    stack_id = serializers.PrimaryKeyRelatedField(queryset=Stack.objects.all(), source='stack', write_only=True)
    stack = StackSerializer(read_only=True)
    
    class Meta:
        model = Worker
        fields = ['id', 'first_name', 'last_name', 'patronymic', 'email', 'user', 'user_id', 'stack', 'stack_id']
        extra_kwargs = {
        'user_id': {'required': False},
    }

#Detail Serializer of the Worker model
class WorkerDetailSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), allow_null=True, source='user', write_only=True)
    user = UserSerializer(read_only=True)
    stack_id = serializers.PrimaryKeyRelatedField(queryset=Stack.objects.all(), source='stack', write_only=True)
    stack = StackSerializer(read_only=True)
    
    class Meta:
        model = Worker
        fields = "__all__"
        extra_kwargs = {
        'user_id': {'required': False},}