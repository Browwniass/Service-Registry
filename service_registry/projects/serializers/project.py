from rest_framework import serializers

from projects.models.project import Project

#Sterilizer of the model Project
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project 
        fields = "__all__"