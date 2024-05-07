from rest_framework import serializers
from statuses.models.status import Status

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status 
        fields = "__all__"
    
class StatusChoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status 
        fields = "__all__"
        read_only_fields = ('name', 'description', 'color')
    