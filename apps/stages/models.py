from django.conf import settings
from django.db import models
from django.utils import timezone


class Stage(models.Model):
    STATUS_CHOICES = [
        ("todo", "Todo"),
        ("in_progress", "In progress"),
        ("done", "Done"),
    ]

    project = models.ForeignKey("projects.Project", related_name="stages", on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    order_index = models.PositiveIntegerField(default=0)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="assigned_stages",
        null=True, blank=True, on_delete=models.SET_NULL,
    )
    required_permission = models.ForeignKey(
        "users.Permission", on_delete=models.PROTECT, related_name="stages",
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="todo")
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["order_index"]

    def mark_done(self):
        self.status = "done"
        self.completed_at = timezone.now()
        self.save(update_fields=["status", "completed_at"])

    def __str__(self):
        return f"{self.project.title} - {self.title}"


class Task(models.Model):
    """Bosqich ichidagi mayda vazifalar (ixtiyoriy, kelajakda kengaytirish uchun)."""

    stage = models.ForeignKey(Stage, related_name="tasks", on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,
    )
    is_done = models.BooleanField(default=False)
    deadline = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
