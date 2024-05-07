from rest_framework import serializers
from references.models.priority import Priority

class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority 
        fields = "__all__"

class PriorityChoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority 
        fields = "__all__"
        read_only_fields = ('name', 'description', 'color')
    