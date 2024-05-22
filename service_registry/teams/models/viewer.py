from django.db.models import Model, ManyToManyField, BooleanField, OneToOneField, CASCADE
from dirtyfields import DirtyFieldsMixin


#The object stores the information necessary to identify the role of the Viewer
class Viewer(DirtyFieldsMixin, Model):
    user = OneToOneField('teams.User', on_delete=CASCADE, related_name="viewer_account")
    is_full = BooleanField(default=False)
    project = ManyToManyField('projects.Project', blank=True, null=True, related_name="viewer_projects")
    
    class Meta:
        app_label = 'teams'

    def __str__(self):
        return f"{self.user}"
    