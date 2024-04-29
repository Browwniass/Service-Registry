from rest_framework import serializers
from references.models.project_type import ProjectType

class ProjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectType 
        fields = "__all__"
    