from rest_framework import serializers
from models.layer import Layer
from rest_framework.utils import model_meta

#Serializer of the model Layer
class LayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Layer
        fields = "__all__"
        
    def update(self, instance, validated_data):
        try:
            comment = self.initial_data['comment']
        except KeyError:
            comment=""

        info = model_meta.get_field_info(instance)

        m2m_fields = []
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)

        instance.save(comment=comment)
        return instance