from rest_framework import serializers
from projects.models.stack import Stack, StackElement

#Detail Serilizer of the model StackElement
class StackElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StackElement
        fields ="__all__"

#Detail Serilizer of the model Stack
class StackSerializer(serializers.ModelSerializer):
    elements = StackElementSerializer(many=True)
    class Meta:
        model = Stack
        fields ="__all__"

