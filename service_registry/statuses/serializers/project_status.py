from rest_framework import serializers
from statuses.models.project_status import ChangeProjectStatus

#Detail Serilizer of the model ProjectDocument
class ChangeProjectStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangeProjectStatus
        fields ="__all__"