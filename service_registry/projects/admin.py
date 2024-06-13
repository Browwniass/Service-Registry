from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(Project)
admin.site.register(Stack)
admin.site.register(StackElement)
admin.site.register(Quarter)
admin.site.register(Layer)
admin.site.register(ProjectDocument)