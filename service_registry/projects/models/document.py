import re
from django.db.models import Model, ForeignKey, CharField, TextField, BooleanField, FileField, CASCADE, SET_NULL
from django.core.exceptions import ValidationError
from dirtyfields import DirtyFieldsMixin


#The object stores information inherent in the project documentation document
class ProjectDocument(DirtyFieldsMixin, Model):
    TYPE_CHOICES =(
        ('t_entry','Введение'),
        ('t_ps','ТЗ'),
        ('t_fun_desc','Функциональное описание'),
        ('t_scheme','Схема'),
        ('t_other','Другое'),
    )

    class Meta:
        app_label = 'projects'

    project = ForeignKey('projects.Project', on_delete = CASCADE)
    prev = ForeignKey('self', on_delete = SET_NULL, null=True, blank=True)
    name = TextField(max_length=500)
    file_type = CharField(max_length=20, choices=TYPE_CHOICES)
    file = FileField(upload_to ='uploads/ProjectDocument')
    file_ver = CharField(max_length=10, help_text="Указывается при помощи 2 чисел разделенных запятой")
    is_visible = BooleanField(default=False)
    
    
    
    #Project validation
    def clean(self):
        reg = r'^\d+,\d+$'
        if not(re.match(reg, self.file_ver)):
            raise ValidationError({'file_ver': "Версия указывается при помощи 2-ух чисел разделенных запятой"})
    
    def save(self, *args, **kwargs):
        self.full_clean()
        #Increasing the document version when it is changed
        if self.pk is not None:
            old = ProjectDocument.objects.get(pk=self.pk)
            old_file = old.file
            if old_file != self.file:
                print(f"Файл обнаружен {self.file_ver+'a'}")
                number_parts = self.file_ver.split(',')#Separation
                part1 = int(number_parts[0])+1#Increase
                part2 = int(number_parts[1])
                full=f"{part1},{part2}"
                #print(f"Файлs {part1} {part2}")
                #Updating the document version
                new_document_inst = ProjectDocument(
                    project=self.project,
                    prev=old,
                    name=self.name,
                    file_type=self.file_type,
                    file=self.file,
                    file_ver=full,
                    is_visible=self.is_visible,
                    )
                new_document_inst.save()
            else:
                return super(ProjectDocument, self).save(*args, **kwargs)
        else: 
            return super(ProjectDocument, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}[{self.project}]"
    