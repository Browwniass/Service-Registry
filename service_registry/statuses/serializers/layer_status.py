from rest_framework import serializers
from statuses.models.layer_status import ChangeLayerStatus

#Detail Serilizer of the model ProjectDocument
class ChangeLayerStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangeLayerStatus
        fields ="__all__"