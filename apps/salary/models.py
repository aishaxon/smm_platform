from django.conf import settings
from django.db import models


class SalaryRule(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="salary_rule",
    )
    base_salary = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    bonus_per_stage = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user} - {self.base_salary}"


class SalaryRecord(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="salary_records", on_delete=models.CASCADE,
    )
    month = models.DateField()
    base_salary = models.DecimalField(max_digits=12, decimal_places=2)
    total_bonus = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_salary = models.DecimalField(max_digits=12, decimal_places=2)
    calculated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "month")

    def __str__(self):
        return f"{self.user} - {self.month} - {self.total_salary}"
