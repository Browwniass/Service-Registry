from django.db.models import Model, ForeignKey, BooleanField, CharField, EmailField, PROTECT, SET_NULL
from django.utils.translation import gettext_lazy as _
from projects.models.stack import Stack
from teams.models.user import User


#The object stores information inherent to the development team employee
class Member(Model):
    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)
    patronymic = CharField(max_length=50, blank=True, null=True)
    email = EmailField(_('email addres'), unique=True) 
    is_archived = BooleanField(default=False)
    user = ForeignKey(User, on_delete=SET_NULL, blank=True, null=True, related_name="team_member_account")
    stack = ForeignKey(Stack, on_delete=PROTECT)
    
    class Meta:
        app_label = 'teams'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}[{self.email}]"
    