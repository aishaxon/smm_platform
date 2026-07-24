from django.contrib import admin
from .models import Stage, Task


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ("title", "project", "assigned_to", "status", "completed_at")
    list_filter = ("status",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "stage", "assigned_to", "is_done")
