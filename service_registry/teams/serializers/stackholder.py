from rest_framework import serializers
from teams.models.stackholder import Stackholder
from teams.models.viewer import Viewer
from teams.serializers.viewer import ViewerSerializer

#Serializer of the model ProjectDocument
class StackholderSerializer(serializers.ModelSerializer):
    viewer_id = serializers.PrimaryKeyRelatedField(queryset=Viewer.objects.all(), source='viewer', write_only=True)
    viewer = ViewerSerializer(read_only=True)
    
    class Meta:
        model = Stackholder
        fields ="__all__"
    