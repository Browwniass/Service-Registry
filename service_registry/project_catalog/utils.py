import sys
from django.db.models.fields.related import ForeignKey
from project_catalog.models import *
from project_catalog.serializers import *

#Getting all instances of fields associated with the model(self) by ForeignKey
def getRelatedFields(self):
    fields = self._meta.get_fields()
    nested_serializers = {}
    for field in fields:#Passing through all fields
        if isinstance(field, ForeignKey):#Stop at related to other models
            related_model = field.related_model
            serializer_name=related_model.__name__+"Serializer"
            serializer_class = getattr(sys.modules[__name__], serializer_name, None)#Getting the serializer class by name
            
            if serializer_class:#Checking for existence before adding to the dictionary
                serializer = serializer_class(instance=related_model.objects.all(), many=True)
                nested_serializers[serializer_name]=serializer.data
    
    return nested_serializers
                