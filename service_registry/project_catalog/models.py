import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
import re
from django.core.exceptions import ValidationError
from django.utils import timezone
from .middleware import current_request

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


class Priority(Manual):
    pass


class ProjectType(Manual):
    pass


class TeamMemberRole(Manual):
    pass


class ProjectComplexity(Manual):
    pass


class LayerType(Manual):
    pass


class ProjectState(Manual):
    pass

#The object stores information characterizing the Quarter
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
       
# The object stores information inherent in the record about the used keyword, language, or library.
class StackElement(models.Model):
    name = models.CharField(max_length=50, unique=True)
    version = models.CharField(max_length=20, unique=True)
    introduced = models.DateField(null=True, blank=True)
    depends_on = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name}[{self.version}]"

#The object stores information characterizing a set of libraries, frameworks, and languages used in development.
class Stack(models.Model):
    name = models.CharField(max_length=50, unique=True)
    elements = models.ManyToManyField(StackElement)

    def __str__(self):
        return f"{self.name}"

#The object stores information inherent in the project as an entity in the designed system.
class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    short_name = models.CharField(max_length=50, unique=True)
    domain = models.CharField(max_length=100, unique=True)
    version = models.CharField(max_length=10, help_text="Указывается при помощи 2 чисел разделенных запятой")
    priority = models.ForeignKey(Priority, on_delete=models.PROTECT)
    complexity = models.ForeignKey(ProjectComplexity, on_delete=models.PROTECT)    
    project_type = models.ForeignKey(ProjectType, on_delete=models.PROTECT)
    quarter = models.ForeignKey(Quarter, on_delete=models.SET_NULL, null=True, blank=True)
    state = models.ForeignKey(ProjectState, on_delete=models.PROTECT)
    stack = models.ForeignKey(Stack, on_delete=models.PROTECT)
    description = models.CharField(max_length=2000, blank=True)
    project_goal = models.CharField(max_length=2000, blank=True)
    project_tasks = models.TextField(blank=True)
    project_functionality = models.TextField(blank=True)
    launch_date = models.DateField(null=True, blank=True)
    history = GenericRelation("HistoryOfChange")
    
    def __str__(self):
        return f"{self.name}[{self.short_name}]"
    
    #Project validation
    def clean(self):
        reg = r'^\d+,\d+$'
        #
        if not(re.match(reg, self.version)):
            raise ValidationError({'version': "Версия указывается при помощи 2-ух чисел разделенных запятой"})
    
    def save(self, *args, **kwargs):
        comment = kwargs.pop('comment', None)
        
        #Logging project with an updated "state"
        if self.pk is not None:
            old_state = Project.objects.get(pk=self.pk).state
            if old_state != self.state:
                #Create comment instance
                comment_instance = Comment.objects.create(
                    project=self,
                    text = comment,
                    created = current_request().user,
                )
                #Create ChangeprojectState instance for logging
                new_state_inst= ChangeProjectState(
                    project=self,
                    state=self.state,
                    comment=comment_instance,
                    installed=current_request().user
                )
                new_state_inst.save()

        self.full_clean()
        return super().save(*args, **kwargs)

#The object stores the information necessary to identify the role of the observer
class Observer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="observer_account")
    is_full = models.BooleanField(default=False)
    project = models.ManyToManyField(Project, blank=True, null=True)

    def __str__(self):
        return f"{self.user}"
    
#The object stores information characterizing the person making decisions or storing information about the project
class Stackholder(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    has_information = models.CharField(max_length=2000)
    contact_information = models.JSONField()
    observer = models.ForeignKey(Observer, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.full_name}[{self.project}]"
    
#The object stores information inherent to the development team employee
class TeamMember(models.Model):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    patronymic = models.CharField(max_length = 50, blank=True, null=True)
    email = models.EmailField(_('email addres'), unique=True) 
    is_archived = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="team_member_account")
    stack = models.ForeignKey(Stack, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.first_name} {self.last_name}[{self.email}]"
    
#The object stores information characterizing a significant part of the project that is allocated to a separate product.
class Layer(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=1000, blank=True)
    link_to_project_in_git = models.URLField(null=True, blank=True)
    link_to_project_in_ser_reg = models.URLField(null=True, blank=True)
    layer_type = models.ForeignKey(LayerType, on_delete=models.PROTECT)
    state = models.ForeignKey(ProjectState, on_delete = models.PROTECT)
    expected_testbed_start_date = models.DateField(null=True, blank=True)
    complexity = models.ForeignKey(ProjectComplexity, on_delete=models.PROTECT)
    stack = models.ForeignKey(Stack, on_delete = models.PROTECT)

    def save(self, *args, **kwargs):
        comment = kwargs.pop('comment', None)
        #Logging project with an updated "state"

        if self.pk is not None:
            old_state = Layer.objects.get(pk=self.pk).state
            if old_state != self.state:
                #Create comment instance
                comment_instance = Comment.objects.create(
                    project=self.project,
                    layer = self,
                    text = comment,
                    created = current_request().user,
                )
                
                #Create ChangeLayerState instance for logging
                new_state_inst= ChangeLayerState(
                    layer=self,
                    state=self.state,
                    comment=comment_instance,
                    installed=current_request().user
                )
                new_state_inst.save()

        self.full_clean()
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name}"
    

#The object stores information characterizing the relationship between the project and the employee involved in its creation
class ProjectEmployeе(models.Model):
    role = models.ForeignKey(TeamMemberRole, on_delete=models.PROTECT) 
    project = models.ForeignKey(Project, on_delete = models.CASCADE, null=True, blank=True)
    layer = models.ForeignKey(Layer, on_delete = models.PROTECT, null=True, blank=True)
    employee = models.ForeignKey(TeamMember, on_delete = models.CASCADE)
    is_application = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=0, null=True, blank=True)
    is_responsible = models.BooleanField(default=False)
    date_joining = models.DateField(null=True, blank=True)
    date_termination = models.DateField(null=True, blank=True)

    def __str__(self):
        print(self.project is None)
        return f"{self.employee}[{self.project}]"

    #Project validation
    def clean(self):
        if self.project is None and self.layer is None:
            raise ValidationError("Должен быть указан или проект или Слой")
        
        if self.is_approved:
            self.date_joining = timezone.localtime(timezone.now())

        if self.employee.is_archived:
            raise ValidationError("Член команды не может быть добавлен к проекту если является архивным")

#The object stores information inherent in the project documentation document
class ProjectDocument(models.Model):
    TYPE_CHOICES =(
        ('t_entry','Введение'),
        ('t_ps','ТЗ'),
        ('t_fun_desc','Функциональное описание'),
        ('t_scheme','Схема'),
        ('t_other','Другое'),
    )

    project = models.ForeignKey(Project, on_delete = models.CASCADE)
    prev = models.ForeignKey('self', on_delete = models.SET_NULL, null=True, blank=True)
    name = models.TextField(max_length=500)
    file_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    file = models.FileField(upload_to ='uploads/ProjectDocument')
    file_ver = models.CharField(max_length=10, help_text="Указывается при помощи 2 чисел разделенных запятой")
    is_visible = models.BooleanField(default=False)
    
    #Project validation
    def clean(self):
        reg = r'^\d+,\d+$'
        if not(re.match(reg, self.file_ver)):
            raise ValidationError({'file_ver': "Версия указывается при помощи 2-ух чисел разделенных запятой"})
    
    def save(self, *args, **kwargs):
        #Increasing the document version when it is changed
        if self.pk is not None:
            old_file = ProjectDocument.objects.get(pk=self.pk).file
            if old_file == self.file:
                print(f"Файл обнаружен {self.file_ver+'a'}")
                number_parts = self.file_ver.split(',')#Separation
                part1 = int(number_parts[0])
                part2 = int(number_parts[1])+1#Increase
                full=f"{part1},{part2}"
                #print(f"Файлs {part1} {part2}")
                #Updating the document version
                new_document_inst = ProjectDocument(
                    project=self.project,
                    prev=self.prev,
                    name=self.name,
                    file_type=self.file_type,
                    file=self.file,
                    file_ver=full,
                    is_visible=self.is_visible,
                    )
                new_document_inst.save()
        else: 
            super(ProjectDocument, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name}[{self.project}]"
    

#The object stores information inherent in a text comment associated with a project, a project layer, or a project document
class Comment(models.Model):
    project = models.ForeignKey(Project, on_delete = models.CASCADE, related_name="comment")
    layer = models.ForeignKey(Layer, on_delete = models.PROTECT, null=True, blank=True)
    document = models.ForeignKey(ProjectDocument, on_delete = models.SET_NULL, null=True, blank=True)
    text = models.TextField(max_length=1000)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_delete = models.DateTimeField(null=True, blank=True)
    date_last_change = models.DateTimeField(auto_now=True)
    created = models.ForeignKey(User, on_delete = models.PROTECT)
    is_hidden = models.BooleanField(default=False) 
    
    def __str__(self):
        return f"{self.created}[{self.date_creation}:{self.project}]"


#The object stores information inherent in the history of changes in the project status
class ChangeProjectState(models.Model):
    project = models.ForeignKey(Project, on_delete = models.CASCADE)
    state = models.ForeignKey(ProjectState, on_delete = models.PROTECT)
    comment = models.ForeignKey(Comment, on_delete = models.SET_NULL, null=True, blank=True)
    date_installation = models.DateTimeField(auto_now=True, unique=True)
    installed = models.ForeignKey(User, on_delete = models.PROTECT)

    def __str__(self):
        return f"{self.project}[{self.date_installation}]"

#Объект хранит информацию присущую истории изменений статуса проекта
class ChangeLayerState(models.Model):
    layer = models.ForeignKey(Layer, on_delete = models.CASCADE)
    state = models.ForeignKey(ProjectState, on_delete = models.PROTECT)
    comment = models.ForeignKey(Comment, on_delete = models.SET_NULL, null=True, blank=True)
    date_installation = models.DateTimeField(auto_now=True, unique=True)
    installed = models.ForeignKey(User, on_delete = models.SET_NULL, null=True, blank=True)
    
    
    def save(self, *args, **kwargs):
        if self.pk is not None:
            old_state = ChangeLayerState.objects.get(pk=self.pk).state
            if old_state != self.state:
                new_state_inst= ChangeLayerState(
                    layer=self.layer,
                    state=self.state,
                    comment=self.comment,
                    date_installation=timezone.localtime(timezone.now()),
                    installed=self.installed
                )
                new_state_inst.save()
        else: 
            super(ChangeLayerState, self).save(*args, **kwargs)


    def __str__(self):
        return f"{self.layer}[{self.date_installation}]"
    
#The object stores information inherent in the history of changes in the project status
class CommentsFile(models.Model):
    comment = models.ForeignKey(Comment, on_delete = models.CASCADE)
    name = models.CharField(max_length=15)
    file = models.FileField(upload_to ='uploads/CommentsFile')

    def clean(self):
        if self.file:
            if self.file.size > 15728640:#Checking if the file does not exceed 15 MB
                raise ValidationError("Максимальный вес загружаемого файла не больше 15 мб")
            if CommentsFile.objects.filter(comment__pk=self.comment.pk).count()>=5:#Checking if more than 5 files per comment have been uploaded
                raise ValidationError("На один комментарий не может быть загружено больше 5 активных файлов")

    def __str__(self):
        return f"{self.name}"
    
#The object stores information characterizing the person making decisions or storing information about the project
class Stackholder(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    has_information = models.CharField(max_length=2000)
    contact_information = models.JSONField()
    observer = models.ForeignKey(Observer, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.full_name}[{self.project}]"
    

#The object stores information inherent in the record of the history of changes to system objects.
class HistoryOfChange(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField(default=uuid.uuid4)
    content_object = GenericForeignKey('content_type', 'object_id')
    value = models.JSONField(blank=True, null=True)
    file = models.FileField(upload_to ='uploads/HistoryOfChange', blank=True, null=True)
    changer = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()      