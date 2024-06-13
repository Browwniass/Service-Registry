from django.db.models import Model, ForeignKey, BooleanField, CharField, EmailField, PROTECT, SET_NULL
from django.utils.translation import gettext_lazy as _
from projects.models.stack import Stack
from django.core.exceptions import ValidationError
from dirtyfields import DirtyFieldsMixin


#The object stores information characterizing the relationship between the project and the employee involved in its creation
class Worker(DirtyFieldsMixin, Model):
    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)
    patronymic = CharField(max_length=50, blank=True, null=True)
    email = EmailField(_('email addres'), unique=True) 
    is_archived = BooleanField(default=False)
    user = ForeignKey('teams.User', on_delete=SET_NULL, blank=True, null=True, related_name="team_member_account")
    stack = ForeignKey('projects.Stack', on_delete=PROTECT)
    
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.__original_is_archived = self.is_archived
            
    class Meta:
        app_label = 'teams'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}[{self.email}]"
    
    def save(self, *args, **kwargs):
        if self.user != None:
            if self.is_archived == True:
                self.user.is_active = False
            else:
                self.user.is_active = True
            self.user.save()
        self.full_clean()
        return super().save(*args, **kwargs)
    
    
"""    #Worker validation
    def clean(self):
        if self.is_archived and self.user.is_active:
            raise ValidationError("Пользовать архивного члена команды должен обязательно быть неактивным")
"""
