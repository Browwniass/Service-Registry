from django.db.models import Model, ForeignKey, BooleanField, DateField, PROTECT, CASCADE
from django.core.exceptions import ValidationError
from django.utils import timezone
from dirtyfields import DirtyFieldsMixin
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken


#The object stores information inherent to the development team employee
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

    #Member validation
    def clean(self):
        if self.project is None and self.layer is None:
            raise ValidationError({'project': "Должен быть указан или проект или Слой"})
        
        if self.worker.is_archived:
            raise ValidationError({'worker': "Член команды не может быть добавлен к проекту если является архивным"})
        
        #Если этот сотрудник уже на проекте, не давать ему добавиться на него еще раз
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
    

"""        elif self.is_approved == False:
            self.date_termination = timezone.localtime(timezone.now()).date()"""