from rest_framework import serializers
from projects.models.project import Project
from projects.models.stack import Stack
from projects.models.quarter import Quarter
from references.models.priority import Priority
from references.models.complexity import Complexity
from references.models.project_type import ProjectType
from statuses.models.status import Status
from projects.serializers.stack import StackSerializer
from projects.serializers.quarter import QuarterSerializer
from references.serializers.priority import PrioritySerializer
from references.serializers.complexity import ComplexitySerializer
from references.serializers.project_type import ProjectTypeSerializer
from statuses.serializers.status import StatusSerializer
from rest_framework.utils import model_meta
#Sterilizer of the model Project
import re

class ProjectSerializer(serializers.ModelSerializer):
    stack_id = serializers.PrimaryKeyRelatedField(queryset=Stack.objects.all(), source='stack', write_only=True)
    stack = StackSerializer(read_only=True)
    priority_id = serializers.PrimaryKeyRelatedField(queryset=Priority.objects.all(), source='priority', write_only=True)
    priority = PrioritySerializer(read_only=True)
    complexity_id = serializers.PrimaryKeyRelatedField(queryset=Complexity.objects.all(), source='complexity', write_only=True)
    complexity = ComplexitySerializer(read_only=True)
    project_type_id = serializers.PrimaryKeyRelatedField(queryset=ProjectType.objects.all(), source='project_type', write_only=True)
    project_type = ProjectTypeSerializer(read_only=True)
    quarter_id = serializers.PrimaryKeyRelatedField(queryset=Quarter.objects.all(), source='quarter', write_only=True)
    quarter = QuarterSerializer(read_only=True)
    status_id = serializers.PrimaryKeyRelatedField(queryset=Status.objects.all(), source='status', write_only=True)
    status = StatusSerializer(read_only=True)

    class Meta:
        model = Project 
        fields = "__all__"
    
    def update(self, instance, validated_data):
        try:
            print(self.initial_data)
            comment = self.initial_data['comment']
        except KeyError:
            comment=""

        info = model_meta.get_field_info(instance)

        m2m_fields = []
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)

        instance.save(comment=comment)
        return instance
    
    def validate_version(self, value):
        reg = r'^\d+,\d+$'
        if not(re.match(reg, value)):
            raise serializers.ValidationError("Версия указывается при помощи 2-ух чисел разделенных запятой")
        return value
