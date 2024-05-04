from rest_framework import serializers
from projects.models.layer import Layer
from rest_framework.utils import model_meta
from references.models.complexity import Complexity
from statuses.models.status import Status
from references.models.layer_type import LayerType
from projects.models.stack import Stack
from projects.serializers.stack import StackSerializer
from references.serializers.complexity import ComplexitySerializer
from references.serializers.layer_type import LayerTypeSerializer
from statuses.serializers.status import StatusSerializer

#Serializer of the model Layer
class LayerSerializer(serializers.ModelSerializer):
    stack_id = serializers.PrimaryKeyRelatedField(queryset=Stack.objects.all(), source='stack', write_only=True)
    stack = StackSerializer(read_only=True)
    status_id = serializers.PrimaryKeyRelatedField(queryset=Status.objects.all(), source='status', write_only=True)
    status = StatusSerializer(read_only=True)
    complexity_id = serializers.PrimaryKeyRelatedField(queryset=Complexity.objects.all(), source='complexity', write_only=True)
    complexity = ComplexitySerializer(read_only=True)
    layer_type_id = serializers.PrimaryKeyRelatedField(queryset=LayerType.objects.all(), source='layer_type', write_only=True)
    layer_type = LayerTypeSerializer(read_only=True)

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