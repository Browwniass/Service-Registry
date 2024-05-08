from rest_framework import serializers
from projects.models.stack import Stack, StackElement


#Detail Serializer of the model StackElement
class StackElementSerializer(serializers.ModelSerializer):
    depends_on_id = serializers.PrimaryKeyRelatedField(queryset=StackElement.objects.all(), source='depends_on', write_only=True, allow_null=True)
    depends_on = serializers.SerializerMethodField(read_only=True)

    def get_depends_on(self, obj):
        if obj.depends_on:
            serializer = StackElementSerializer(obj.depends_on)
            return serializer.data
        return None
    
    class Meta:
        model = StackElement
        fields ="__all__"

#Detail Serilizer of the model Stack
class StackSerializer(serializers.ModelSerializer):
    elements_id = serializers.PrimaryKeyRelatedField(queryset=StackElement.objects.all(), source='elements', many=True, write_only=True)
    elements = StackElementSerializer(many=True, read_only=True)

    class Meta:
        model = Stack
        fields ="__all__"


#Detail Serializer of the model Stack
class StackChoicesSerializer(serializers.ModelSerializer):
    elements = StackElementSerializer(many=True, read_only=True)

    class Meta:
        model = Stack
        fields = ['name', 'elements']
        read_only_fields = ['name']
