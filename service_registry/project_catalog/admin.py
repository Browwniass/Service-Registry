from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)

admin.site.register(Priority)
admin.site.register(ProjectComplexity)
admin.site.register(ProjectType)
admin.site.register(Quarter)
admin.site.register(ProjectState)
admin.site.register(Project)
admin.site.register(Stack)
admin.site.register(StackElement)
admin.site.register(Observer)
admin.site.register(TeamMember)
admin.site.register(ProjectEmployeе)
admin.site.register(Layer)
admin.site.register(ChangeLayerState)
admin.site.register(Comment)
admin.site.register(CommentsFile)
admin.site.register(ChangeProjectState)
admin.site.register(ProjectDocument)
admin.site.register(HistoryOfChange)

