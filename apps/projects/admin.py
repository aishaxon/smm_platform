from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "client", "pm", "status", "created_at")
    list_filter = ("status",)
