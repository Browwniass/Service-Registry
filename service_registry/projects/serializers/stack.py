from rest_framework import serializers
from projects.models.stack import Stack, StackElement


#Detail Serializer of the model StackElement
class StackElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StackElement
        fields ="__all__"


#Detail Serilizer of the model Stack
class StackSerializer(serializers.ModelSerializer):
    #elements = StackElementSerializer(many=True, read_only=True, source='elements')
    elements_id = serializers.PrimaryKeyRelatedField(queryset=StackElement.objects.all(), source='elements', many=True, write_only=True)
    elements = StackElementSerializer(read_only=True, many=True)
    
    class Meta:
        model = Stack
        fields ="__all__"


#Choices Serializer of the model Stack
class StackChoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stack
        fields = ['id', 'name']
        read_only_fields = ['id', 'name']


#Choices Serializer of the model StackElement
class StackElementChoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = StackElement
        fields = ['id', 'name', 'version']
        read_only_fields = ['id', 'name', 'version']
