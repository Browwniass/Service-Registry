from rest_framework import serializers
from .models import *
import re
from rest_framework.utils import model_meta

#Sterilizer of the User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

#Sterilizer of the Observer model
class ObserverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Observer
        fields = "__all__"

    def validate(self, data):
        if data['is_full'] and len(data['project']) != 0:
            raise serializers.ValidationError("К Полному Наблюдателя нельзя добавлять проекты")
        return data


#Sterilizer of the TeamMember model
class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = "__all__"

#Sterilizer of the model ProjectEmployeе
class ProjectEmployeеSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectEmployeе
        fields = "__all__"

#Sterilizer of the model Priority
class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = ["name"]

#Sterilizer of the model Project
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project 
        fields = "__all__"

    #Presentation of projects in a readable form when sending
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['priority'] = instance.priority.name
        return representation

    def update(self, instance, validated_data):
        try:
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

#Sterilizer of the model ProjectType
class ProjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = "__all__"

#Sterilizer of the model ProjectType
class TeamMemberRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMemberRole
        fields = "__all__"

#Sterilizer of the model ProjectType
class ProjectComplexitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectComplexity
        fields = "__all__"

#Sterilizer of the model ProjectType
class LayerTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerType
        fields = "__all__"

#Sterilizer of the model ProjectType
class ProjectStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectState
        fields = "__all__"


#Sterilizer of the model Quarter
class QuarterSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    year = serializers.IntegerField()
    quarter = serializers.ChoiceField(choices=Quarter.QUARTER_CHOICES)

    def create(self, validated_data):
        return Quarter.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.year = validated_data.get('year', instance.year)
        instance.quarter = validated_data.get('quarter', instance.quarter)
        instance.save()
        return instance

#Sterilizer of the model Layer
class LayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Layer
        fields = "__all__"
        
    def update(self, instance, validated_data):
        try:
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
#Sterilizer of the model Comment
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['project', 'layer', 'document', 'text', 'created']

#Sterilizer of the model
class CommentsFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentsFile
        fields ="__all__"

#Sterilizer of the model ProjectDocument
class ProjectDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDocument
        fields ="__all__"