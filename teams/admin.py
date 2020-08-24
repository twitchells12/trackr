from django.contrib import admin
from . import models

# Register your models here.
class TeamInline(admin.TabularInline):
    model = models.Team.members.through

class TeamAdmin(admin.ModelAdmin):
    inlines = (TeamInline,)

admin.site.register(models.Team,TeamAdmin)
