from rest_framework import serializers
from references.models.layer_type import LayerType

class LayerTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerType 
        fields = "__all__"
    