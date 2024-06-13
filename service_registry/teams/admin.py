from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Viewer)
admin.site.register(Member)
admin.site.register(Stackholder)
admin.site.register(Worker)

