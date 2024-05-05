from rest_framework import serializers
from .models import *
from projects.models.layer import Layer
from projects.serializers.layer import LayerSerializer
from teams.models.user import User
from teams.serializers.user import UserSerializer

#Serializer of the model Comment
class CommentListSerializer(serializers.ModelSerializer):
    layer_id = serializers.PrimaryKeyRelatedField(queryset=Layer.objects.all(), source='layer', write_only=True)
    layer = LayerSerializer(read_only=True)
    created = UserSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'project', 'document', 'created', 'text', 'layer', 'layer_id']
        
#Serializer of the model Comment
class CommentDetailSerializer(serializers.ModelSerializer):
    layer_id = serializers.PrimaryKeyRelatedField(queryset=Layer.objects.all(), source='layer', write_only=True)
    layer = LayerSerializer(read_only=True)
    created = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ['date_creation', 'date_delete', 'date_last_change']
        
#Serializer of the model File
class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields ="__all__"