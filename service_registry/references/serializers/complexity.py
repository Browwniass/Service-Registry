from rest_framework import serializers
from references.models.complexity import Complexity

class ComplexitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Complexity 
        fields = "__all__"
    
class ComplexityChoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complexity 
        fields = "__all__"
        read_only_fields = ('name', 'description', 'color')
    