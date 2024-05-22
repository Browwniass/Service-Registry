from django.contrib.auth.models import AbstractUser
from django.db.models import EmailField, CharField
from django.utils.translation import gettext_lazy as _
from dirtyfields import DirtyFieldsMixin


# User Model
class User(DirtyFieldsMixin, AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('ordinary', 'Ordinary')
    )
    email = EmailField(_('email addres'), unique=True) 
    role = CharField(max_length=25, choices=ROLE_CHOICES, default=ROLE_CHOICES[1])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        app_label = 'teams'
    
    def __str__(self):
        return f"{self.email}[{self.role}]"
    