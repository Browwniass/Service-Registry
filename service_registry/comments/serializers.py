from rest_framework import serializers
from .models import *
from projects.models.layer import Layer
from projects.serializers.layer import LayerSerializer
from teams.models.user import User
from teams.serializers.user import UserSerializer

#Serializer of the model Comment
class CommentListSerializer(serializers.ModelSerializer):
    created = UserSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'project', 'document', 'created', 'text', 'date_creation', 'date_last_change', 'project']
        read_only_fields = ['date_creation', 'date_last_change', 'project']

        
#Serializer of the model Comment
class CommentDetailSerializer(serializers.ModelSerializer):
    created = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        exclude = ['layer', 'project']
        read_only_fields = ['date_creation', 'date_delete', 'date_last_change', 'project']
        
#Serializer of the model File
class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields ="__all__"