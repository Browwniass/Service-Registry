from django.db.models import Model, ForeignKey, CharField, JSONField, SET_NULL, CASCADE


#The object stores information characterizing the person making decisions or storing information about the project
class Stackholder(Model):
    project = ForeignKey('projects.Project', on_delete=CASCADE)
    full_name = CharField(max_length=200)
    organization = CharField(max_length=200)
    has_information = CharField(max_length=2000)
    contact_information = JSONField()
    viewer = ForeignKey('teams.Viewer', on_delete=SET_NULL, blank=True, null=True)
    
    class Meta:
        app_label = 'teams'
    
    def __str__(self):
        return f"{self.full_name}[{self.project}]"
    