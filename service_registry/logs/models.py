import uuid
from django.db.models import Model, ForeignKey, UUIDField, JSONField, FileField, DateTimeField, CASCADE
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


#The object stores information inherent in the record of the history of changes to system objects.
class HistoryOfChange(Model):
    content_type = ForeignKey(ContentType, on_delete=CASCADE)
    object_id = UUIDField(default=uuid.uuid4)
    content_object = GenericForeignKey('content_type', 'object_id')
    value = JSONField(blank=True, null=True)
    file = FileField(upload_to ='uploads/HistoryOfChange', blank=True, null=True)
    changer = ForeignKey('teams.User', on_delete=CASCADE)
    date = DateTimeField()      