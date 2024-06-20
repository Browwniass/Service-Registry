from django.db.models import Model, CharField, ForeignKey, DateField, TextField, PROTECT, SET_NULL
from django.utils.translation import gettext_lazy as _
import re
from django.core.exceptions import ValidationError
from logs.middleware import current_request
from statuses.models.project_status import ChangeProjectStatus
from comments.models import Comment
from teams.models.user import User
from django.contrib.contenttypes.fields import GenericRelation
from dirtyfields import DirtyFieldsMixin

#The object stores information inherent in the project as an entity in the designed system.
class Project(DirtyFieldsMixin, Model):
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
        
        #Logging project with an updated "status"
        if self.pk is not None:
            old_status = Project.objects.get(pk=self.pk).status
            #print(f"old: {old_status}\n new: {self.status}")
            if old_status != self.status:
                #Create comment instance
                if comment == '':
                    comment_instance = None
                else: 
                    comment_instance = Comment.objects.create(
                    project = self,
                    text = comment,
                    created = current_request().user,
                )
                #Create ChangeprojectStatus instance for logging
                new_status_inst = ChangeProjectStatus(
                    project = self,
                    status = self.status,
                    comment = comment_instance,
                    installed = current_request().user
                )
                new_status_inst.save()

        self.full_clean()
        
        return super().save(*args, **kwargs)


#current_request().user