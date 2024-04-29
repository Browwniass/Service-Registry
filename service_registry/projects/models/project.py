from django.db.models import Model, CharField, ForeignKey, DateField, TextField, PROTECT, SET_NULL
from django.utils.translation import gettext_lazy as _
import re
from django.core.exceptions import ValidationError
from logs.middleware import current_request
from statuses.models.project_status import ChangeProjectStatus
from comments.models import Comment
from django.contrib.contenttypes.fields import GenericRelation

#The object stores information inherent in the project as an entity in the designed system.
class Project(Model):
    name = CharField(max_length=100, unique=True)
    short_name = CharField(max_length=50, unique=True)
    domain = CharField(max_length=100, unique=True)
    version = CharField(max_length=10, help_text="Указывается при помощи 2 чисел разделенных запятой")
    priority = ForeignKey('references.Priority', on_delete=PROTECT)
    complexity = ForeignKey('references.Complexity', on_delete=PROTECT)    
    project_type = ForeignKey('references.ProjectType', on_delete=PROTECT)
    quarter = ForeignKey('projects.Quarter', on_delete=SET_NULL, null=True, blank=True)
    status = ForeignKey('statuses.Status', on_delete=PROTECT)
    stack = ForeignKey('projects.Stack', on_delete=PROTECT)
    description = CharField(max_length=2000, blank=True)
    project_goal = CharField(max_length=2000, blank=True)
    project_tasks = TextField(blank=True)
    project_functionality = TextField(blank=True)
    launch_date = DateField(null=True, blank=True)
    history = GenericRelation("logs.HistoryOfChange")
    
    class Meta:
        app_label = 'projects'

    def __str__(self):
        return f"{self.name}[{self.short_name}]"
    
    #Project validation
    def clean(self):
        reg = r'^\d+,\d+$'
        #
        if not(re.match(reg, self.version)):
            raise ValidationError({'version': "Версия указывается при помощи 2-ух чисел разделенных запятой"})
    
    def save(self, *args, **kwargs):
        comment = kwargs.pop('comment', None)
        
        #Logging project with an updated "state"
        if self.pk is not None:
            old_state = Project.objects.get(pk=self.pk).state
            if old_state != self.state:
                #Create comment instance
                comment_instance = Comment.objects.create(
                    project=self,
                    text = comment,
                    created = current_request().user,
                )
                #Create ChangeprojectState instance for logging
                new_state_inst= ChangeProjectStatus(
                    project=self,
                    state=self.state,
                    comment=comment_instance,
                    installed=current_request().user
                )
                new_state_inst.save()

        self.full_clean()
        return super().save(*args, **kwargs)
