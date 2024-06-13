from rest_framework import serializers
from statuses.models.layer_status import ChangeLayerStatus
from statuses.serializers.status import StatusChoicesSerializer
from projects.serializers.project import ProjectChoiceSerializer
from teams.serializers.user import UserListSerializer


#Detail Serilizer of the model ProjectDocument
class ChangeLayerStatusSerializer(serializers.ModelSerializer):
    installed = UserListSerializer(read_only=True)
    status = StatusChoicesSerializer(read_only=True)
    comment = serializers.SlugRelatedField(
            read_only=True,
            slug_field='text'
    )

    class Meta:
        model = ChangeLayerStatus
        fields ="__all__"
        read_only_fields = ['layers']