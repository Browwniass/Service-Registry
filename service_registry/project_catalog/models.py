from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


# User Model
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('ordinary', 'Ordinary')
    )
    email = models.EmailField(_('email addres'), unique=True) 
    role = models.CharField(max_length=25, choices=ROLE_CHOICES, default=ROLE_CHOICES[1])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.email}[{self.role}]"
    
#Abstract class for all reference books
class Manual(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=1000)
    color = models.CharField(max_length=6)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.name}[{self.color}]"
       
#The directory object is the priority available for selection in the project.
class Priority(Manual):
    pass

#The directory object is the type of project available for selection in the project.
class ProjectType(Manual):
    pass

#The directory object is the role of a team member available for selection in the employee data.
class TeamMemberRole(Manual):
    pass

#The object of the directory is the complexity of the project available for selection in the project.
class ProjectComplexity(Manual):
    pass

#The reference object is the type of layer available for selection in the layer data.
class LayerType(Manual):
    pass

#The reference object is the type of states available for selection in the State data.
class ProjectState(Manual):
    pass

#The object stores information characterizing the planning quarter
class Quarter(models.Model):
    QUARTER_CHOICES =(
        ('q1','Q1'),
        ('q2','Q2'),
        ('q3','Q3'),
        ('q4','Q4'),
    )
    year = models.IntegerField()
    quarter = models.CharField(max_length=4, choices=QUARTER_CHOICES)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['year', 'quarter'], name='quarter_constr')]
    
    def __str__(self):
        return f"{self.year}[{self.quarter}]"
       