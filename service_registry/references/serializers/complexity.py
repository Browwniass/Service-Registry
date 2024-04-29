from rest_framework import serializers
from references.models.complexity import Complexity

class ComplexitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Complexity 
        fields = "__all__"
    