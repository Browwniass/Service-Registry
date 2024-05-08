from rest_framework import serializers
from projects.models.quarter import Quarter

#Detail Serilizer of the model Quarter
class QuarterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quarter
        fields = "__all__"

#Detail Serilizer of the model Quarter
class QuarterChoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quarter
        fields = "__all__"
        read_only_fields = ['year', 'quarter']

