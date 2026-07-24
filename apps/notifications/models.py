from django.conf import settings
from django.db import models


class Notification(models.Model):
    TYPE_CHOICES = [
        ("stage_assigned", "Stage assigned"),
        ("stage_done", "Stage done"),
        ("salary", "Salary"),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="notifications", on_delete=models.CASCADE,
    )
    message = models.TextField()
    notif_type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    is_read = models.BooleanField(default=False)
    sent_via_telegram = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.notif_type}"
