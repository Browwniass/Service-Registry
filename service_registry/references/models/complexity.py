from django.db.models import Model, CharField, TextField
from dirtyfields import DirtyFieldsMixin

class Complexity(DirtyFieldsMixin, Model):
    name = CharField(max_length=100, unique=True)
    description = TextField(max_length=1000)
    color = CharField(max_length=6)

    class Meta:
        app_label = 'references'

    def __str__(self):
        return f"{self.name}[{self.color}]"
