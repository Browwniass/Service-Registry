from rest_framework import serializers
from teams.models.viewer import Viewer
from projects.models.project import Project
from teams.models.user import User
from teams.serializers.user import UserListSerializer
from projects.serializers.project import ProjectSerializer, ProjectChoiceSerializer

#Serializer of the model Viewer
class AdminViewerSerializer(serializers.ModelSerializer):
    #project_id = ProjectSerializer(many=True, read_only=True, source='project')
    project_id = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), many=True, source='project', write_only=True)
    project = ProjectChoiceSerializer(read_only=True, many=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True)
    user = UserListSerializer(read_only=True)
    
    class Meta:
        model = Viewer
        fields ="__all__"

    def validate(self, data):
        if data['is_full'] and len(data['project']) != 0:
            raise serializers.ValidationError("К Полному Наблюдателя нельзя добавлять проекты")
        return data

    
class ProjectViewerSerializer(serializers.ModelSerializer):
    project = ProjectChoiceSerializer(read_only=True, many=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True)
    user = UserListSerializer(read_only=True)

    class Meta:
        model = Viewer
        fields = '__all__'

    
    def validate(self, data):
        if data['is_full'] and len(data['project']) != 0:
            raise serializers.ValidationError("К Полному Наблюдателя нельзя добавлять проекты")
        return data

class ViewerListSerializer(serializers.ModelSerializer):
    user = UserListSerializer(read_only=True)

    class Meta:
        model = Viewer
        fields =['user']
        read_only_fields = ['user']