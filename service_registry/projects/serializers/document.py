from rest_framework import serializers
from projects.models.document import ProjectDocument


class ProjectDocumentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDocument
        fields =['id', 'name', 'file_type', 'file', 'file_ver']
        read_only_fields = ['project', 'prev']


class ProjectDocumentDetailSerializer(serializers.ModelSerializer):
    prev = serializers.SlugRelatedField(
        read_only=True,
        slug_field='prev'
    )

    class Meta:
        model = ProjectDocument
        fields = ['id', 'name', 'file_type', 'file', 'file_ver', 'is_visible', 'prev']
        read_only_fields = ['project', 'prev']