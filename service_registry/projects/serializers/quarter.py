from rest_framework import serializers
from projects.models.quarter import Quarter


class QuarterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quarter
        fields = "__all__"
        read_only_fields = ['quarter']
    

class QuarterChoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quarter
        fields = "__all__"
        read_only_fields = ['year', 'quarter']

