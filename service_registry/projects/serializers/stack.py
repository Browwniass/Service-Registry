from rest_framework import serializers
from projects.models.stack import Stack, StackElement


class StackElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StackElement
        fields ="__all__"


class StackSerializer(serializers.ModelSerializer):
    elements_id = serializers.PrimaryKeyRelatedField(queryset=StackElement.objects.all(), source='elements', many=True, write_only=True)
    elements = StackElementSerializer(read_only=True, many=True)
    
    class Meta:
        model = Stack
        fields ="__all__"


class StackChoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stack
        fields = ['id', 'name']
        read_only_fields = ['id', 'name']


class StackElementChoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = StackElement
        fields = ['id', 'name', 'version']
        read_only_fields = ['id', 'name', 'version']
