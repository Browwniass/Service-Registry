from rest_framework import serializers
from .models import *

#Serializer of the model Comment
class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['project', 'layer', 'document', 'text', 'created']
    
#Serializer of the model Comment
class CommentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__al__"
        
#Serializer of the model File
class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields ="__all__"