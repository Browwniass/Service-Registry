from django.db.models import Model, ForeignKey, DateTimeField, TextField, BooleanField, CharField, FileField, PROTECT, CASCADE, SET_NULL
from django.core.exceptions import ValidationError


#The object stores information inherent in a text comment associated with a project, a project layer, or a project document
class Comment(Model):
    project = ForeignKey('projects.Project', on_delete = CASCADE, related_name="comment")
    layer = ForeignKey('projects.Layer', on_delete = PROTECT, null=True, blank=True)
    document = ForeignKey('projects.ProjectDocument', on_delete = SET_NULL, null=True, blank=True)
    text = TextField(max_length=1000)
    date_creation = DateTimeField(auto_now_add=True)
    date_delete = DateTimeField(null=True, blank=True)
    date_last_change = DateTimeField(auto_now=True)
    created = ForeignKey('teams.User', on_delete = PROTECT)
    is_hidden = BooleanField(default=False) 
    
    def __str__(self):
        return f"{self.created}[{self.date_creation}:{self.project}]"
    
#The object stores information inherent in the history of changes in the project status
class File(Model):
    comment = ForeignKey(Comment, on_delete = CASCADE)
    name = CharField(max_length=15)
    file = FileField(upload_to='uploads/Comments/File')

    def clean(self):
        if self.file:
            if self.file.size > 15728640:#Checking if the file does not exceed 15 MB
                raise ValidationError("Максимальный вес загружаемого файла не больше 15 мб")
            if File.objects.filter(comment__pk=self.comment.pk).count()>=5:#Checking if more than 5 files per comment have been uploaded
                raise ValidationError("На один комментарий не может быть загружено больше 5 активных файлов")

    def __str__(self):
        return f"{self.name}"
    