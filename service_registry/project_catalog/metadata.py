from rest_framework.relations import ManyRelatedField
from rest_framework.metadata import SimpleMetadata, BaseMetadata
from rest_framework.relations import ManyRelatedField, RelatedField


class OptionWithChoices(SimpleMetadata):

    def get_field_info(self, field):
        field_info = super(OptionWithChoices, self).get_field_info(field)
        
        if isinstance(field, RelatedField):
            field_info['choices'] = field.get_choices()
        return field_info

