from django.db.models import Model, ForeignKey, BooleanField, DateField, PROTECT, CASCADE
from django.core.exceptions import ValidationError
from django.utils import timezone
from dirtyfields import DirtyFieldsMixin


class Member(DirtyFieldsMixin, Model):
    role = ForeignKey('references.MemberRole', on_delete = PROTECT) 
    project = ForeignKey('projects.Project', on_delete = CASCADE, null=True, blank=True)
    layer = ForeignKey('projects.Layer', on_delete = PROTECT, null=True, blank=True)
    worker = ForeignKey('teams.Worker', on_delete = CASCADE)
    is_application = BooleanField(default=False)
    is_approved = BooleanField(default=None, null=True, blank=True)
    is_responsible = BooleanField(default=False)
    date_joining = DateField(null=True, blank=True)
    date_termination = DateField(null=True, blank=True)
    
    class Meta:
        app_label = 'teams'
    
    def __str__(self):
        return f"{self.worker}[{self.project}]"

    # Member validation
    def clean(self):
        if self.project is None and self.layer is None:
            raise ValidationError({'project': "Either the project or the Layer must be specified"})
        if self.worker.is_archived:
            raise ValidationError({'worker': "A team member cannot be added to a project if it is archived"})
        
        # If this Member is already on the project, do not let him be added to it again
        if self.project != None and Member.objects.filter(project=self.project, worker=self.worker).exists():
            if not self.pk:
                raise ValidationError({'project': 'There is already an member with this project'})
            elif self.pk:
                member_project = Member.objects.filter(pk=self.pk)
                if self.worker.id != member_project.values_list('worker', flat=True)[0]:
                    raise ValidationError({'project': 'da fuck is already an member with this project'})
            
    def save(self, *args, **kwargs):
        # If member application is approved, then set date_joining
        if self.is_approved:
            self.date_joining = timezone.localtime(timezone.now()).date()
            self.date_termination = None
        
        self.full_clean()    

        return super().save(*args, **kwargs)
    
