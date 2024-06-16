from django.db.models import Model, ManyToManyField, BooleanField, OneToOneField, CASCADE
from dirtyfields import DirtyFieldsMixin
from django.forms import ValidationError
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken


class Viewer(DirtyFieldsMixin, Model):
    user = OneToOneField('teams.User', on_delete=CASCADE, related_name="viewer_account")
    is_full = BooleanField(default=False)
    project = ManyToManyField('projects.Project', blank=True, null=True, related_name="viewer_projects")
    
    class Meta:
        app_label = 'teams'
    
    def save(self, *args, **kwargs):
        # Only when assigning the role blacklist token
        if self.pk == None:
            tokens = OutstandingToken.objects.filter(user=self.user)
            for token in tokens:
                try:
                    # Adding each token to the blacklist
                    BlacklistedToken.objects.get_or_create(token=token)
                except Exception as e:
                    raise ValidationError(f"Error blacklisting token")
        return super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        tokens = OutstandingToken.objects.filter(user=self.user)
        for token in tokens:
            try:
                # Adding each token to the blacklist
                BlacklistedToken.objects.get_or_create(token=token)
            except Exception as e:
                raise ValidationError(f"Error blacklisting token")
        return super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.user}"
    