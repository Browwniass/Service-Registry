from rest_framework import serializers
from projects.models.document import ProjectDocument

#List Serilizer of the model ProjectDocument
class ProjectDocumentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDocument
        fields =['id', 'project', 'name', 'file_type', 'file', 'file_ver']


#Detail Serilizer of the model ProjectDocument
class ProjectDocumentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDocument
        fields ="__all__"