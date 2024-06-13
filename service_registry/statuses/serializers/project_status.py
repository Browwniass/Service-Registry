from rest_framework import serializers
from statuses.models.project_status import ChangeProjectStatus
from statuses.serializers.status import StatusChoicesSerializer
from projects.serializers.project import ProjectChoiceSerializer
from teams.serializers.user import UserListSerializer


#Serializer of the model ChangeProjectStatus
class ChangeProjectStatusSerializer(serializers.ModelSerializer):
    installed = UserListSerializer(read_only=True)
    status = StatusChoicesSerializer(read_only=True)
    comment = serializers.SlugRelatedField(
            read_only=True,
            slug_field='text'
    )

    class Meta:
        model = ChangeProjectStatus
        exclude = ['project']