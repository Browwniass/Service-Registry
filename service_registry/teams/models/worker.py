from django.db.models import Model, ForeignKey, BooleanField, CharField, EmailField, PROTECT, SET_NULL
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from dirtyfields import DirtyFieldsMixin
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken


#The object stores information characterizing the relationship between the project and the employee involved in its creation
class Worker(DirtyFieldsMixin, Model):
    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)
    patronymic = CharField(max_length=50, blank=True, null=True)
    email = EmailField(_('email addres'), unique=True) 
    is_archived = BooleanField(default=False)
    user = ForeignKey('teams.User', on_delete=SET_NULL, blank=True, null=True, related_name="team_member_account")
    stack = ForeignKey('projects.Stack', on_delete=PROTECT)
    

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

            # Only when assigning the role blacklist token
            if self.pk == None:
                # Blacklist token after changes in user model
                tokens = OutstandingToken.objects.filter(user=self.user)
                for token in tokens:
                    try:
                        # Adding each token to the blacklist
                        BlacklistedToken.objects.get_or_create(token=token)
                    except Exception as e:
                        raise ValidationError(f"Error blacklisting token")
            
        self.full_clean()
        
        return super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        if self.user != None:
            tokens = OutstandingToken.objects.filter(user=self.user)
            for token in tokens:
                try:
                    # Adding each token to the blacklist
                    BlacklistedToken.objects.get_or_create(token=token)
                except Exception as e:
                    raise ValidationError(f"Error blacklisting token")
            
        return super().delete(*args, **kwargs)