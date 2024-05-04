from django.db.models import Model, ForeignKey, BooleanField, DateField, PROTECT, CASCADE
from django.core.exceptions import ValidationError
from django.utils import timezone


#The object stores information inherent to the development team employee
class Member(Model):
    role = ForeignKey('references.MemberRole', on_delete = PROTECT) 
    project = ForeignKey('projects.Project', on_delete = CASCADE, null=True, blank=True)
    layer = ForeignKey('projects.Layer', on_delete = PROTECT, null=True, blank=True)
    worker = ForeignKey('teams.Worker', on_delete = CASCADE)
    is_application = BooleanField(default=False)
    is_approved = BooleanField(default=0, null=True, blank=True)
    is_responsible = BooleanField(default=False)
    date_joining = DateField(null=True, blank=True)
    date_termination = DateField(null=True, blank=True)
    
    class Meta:
        app_label = 'teams'
    
    def __str__(self):
        print(self.project is None)
        return f"{self.worker}[{self.project}]"

    #Project validation
    def clean(self):
        if self.project is None and self.layer is None:
            raise ValidationError("Должен быть указан или проект или Слой")
        
        if self.is_approved:
            self.date_joining = timezone.localtime(timezone.now())

        if self.worker.is_archived:
            raise ValidationError("Член команды не может быть добавлен к проекту если является архивным")

    