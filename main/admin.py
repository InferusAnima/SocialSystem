from django.contrib import admin
from .models import Task, Profile, Benefit

# Register your models here.
admin.site.register(Task)
admin.site.register(Profile)
admin.site.register(Benefit)
