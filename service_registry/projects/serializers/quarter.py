from rest_framework import serializers
from projects.models.quarter import Quarter

#Detail Serilizer of the model Quarter
class QuarterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quarter
        fields ="__all__"

