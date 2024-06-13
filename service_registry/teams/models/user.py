from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db.models import EmailField, BooleanField
from django.utils.translation import gettext_lazy as _
from dirtyfields import DirtyFieldsMixin


class MyUserManager(BaseUserManager):
    def create_user(self, email, password, username, **other_fields):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username, **other_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, **other_fields):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        user = self.create_user(email,
            password=password,
            username=username, **other_fields
        )

        user.is_admin = True
        user.save(using=self._db)
        return user


# User Model
class User(DirtyFieldsMixin, AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('ordinary', 'Ordinary')
    )
    is_admin = BooleanField(default=False)
    email = EmailField(_('email addres'), unique=True) 

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        app_label = 'teams'
    

    def __str__(self):
        return f"{self.email}"

         
    