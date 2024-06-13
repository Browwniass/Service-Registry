from rest_framework import serializers
from logs.models import HistoryOfChange

#Detail Serilizer of the model ProjectDocument
class HistoryOfChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoryOfChange
        fields ="__all__"