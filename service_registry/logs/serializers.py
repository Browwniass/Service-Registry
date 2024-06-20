from rest_framework import serializers
from logs.models import HistoryOfChange
from teams.serializers.user import UserChoiceSerializer


#Detail Serilizer of the model HistoryOfChange
class HistoryOfChangeSerializer(serializers.ModelSerializer):
    changer = UserChoiceSerializer()
    content_type_name = serializers.SerializerMethodField()

    class Meta:
        model = HistoryOfChange
        exclude = ['content_type', 'object_id']

    def get_content_type_name(self, obj):
        return obj.content_type.model_class()._meta.verbose_name