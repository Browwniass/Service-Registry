from rest_framework import serializers
from references.models.project_type import ProjectType


class ProjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectType 
        fields = "__all__"


class ProjectTypeChoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectType 
        fields = "__all__"
        read_only_fields = ('name', 'color')
    