from django.conf import settings
from django.db import models


class Project(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("completed", "Completed"),
        ("paused", "Paused"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="projects",
        on_delete=models.CASCADE, limit_choices_to={"role": "client"},
    )
    pm = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="managed_projects",
        on_delete=models.SET_NULL, null=True, blank=True,
        limit_choices_to={"role": "pm"},
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="created_projects",
        on_delete=models.SET_NULL, null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def progress_percent(self) -> int:
        total = self.stages.count()
        if total == 0:
            return 0
        done = self.stages.filter(status="done").count()
        return round(done / total * 100)

    def __str__(self):
        return self.title
