from django.db.models import Model, CharField, ManyToManyField, ForeignKey, DateField, SET_NULL
from django.contrib.contenttypes.fields import GenericRelation
from dirtyfields import DirtyFieldsMixin


# The object stores information inherent in the record about the used keyword, language, or library.
class StackElement(DirtyFieldsMixin, Model):
    name = CharField(max_length=50)
    version = CharField(max_length=20)
    introduced = DateField(null=True, blank=True)
    depends_on = ForeignKey('self', on_delete=SET_NULL, null=True, blank=True)

    class Meta:
        app_label = 'projects'
        unique_together = ('name', 'version',)

    def __str__(self):
        return f"{self.name}[{self.version}]"

#The object stores information characterizing a set of libraries, frameworks, and languages used in development.
class Stack(DirtyFieldsMixin, Model):
    ENABLE_M2M_CHECK = True
    name = CharField(max_length=50, unique=True)
    elements = ManyToManyField(StackElement, related_name='elements')
    history = GenericRelation("logs.HistoryOfChange")
    
    class Meta:
        app_label = 'projects'

    def __str__(self):
        return f"{self.name}"