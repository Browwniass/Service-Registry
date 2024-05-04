from rest_framework import serializers
from teams.models.stackholder import Stackholder
from teams.models.viewer import Viewer

#Serializer of the model ProjectDocument
class ViewerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Viewer
        fields ="__all__"
    