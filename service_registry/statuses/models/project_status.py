from django.db.models import Model, ForeignKey, DateTimeField, PROTECT, CASCADE, SET_NULL

#The object stores information inherent in the history of changes in the project status
class ChangeProjectStatus(Model):
    project = ForeignKey('projects.project', on_delete = CASCADE)
    status = ForeignKey('statuses.Status', on_delete = PROTECT)
    comment = ForeignKey('comments.Comment', on_delete = SET_NULL, null=True, blank=True)
    date_installation = DateTimeField(auto_now=True, unique=True)
    installed = ForeignKey('teams.User', on_delete = PROTECT)
        
    class Meta:
        app_label = 'statuses'

    def __str__(self):
        return f"{self.project}[{self.date_installation}]"