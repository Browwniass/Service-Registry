from django.db.models import Model, ManyToManyField, BooleanField, OneToOneField, CASCADE


#The object stores the information necessary to identify the role of the observer
class Viewer(Model):
    user = OneToOneField('teams.User', on_delete=CASCADE, related_name="viewer_account")
    is_full = BooleanField(default=False)
    project = ManyToManyField('projects.Project', blank=True)
    
    class Meta:
        app_label = 'teams'
    
    def __str__(self):
        return f"{self.user}"