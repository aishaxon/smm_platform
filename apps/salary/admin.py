from django.contrib import admin
from .models import SalaryRule, SalaryRecord


@admin.register(SalaryRule)
class SalaryRuleAdmin(admin.ModelAdmin):
    list_display = ("user", "base_salary", "bonus_per_stage")


@admin.register(SalaryRecord)
class SalaryRecordAdmin(admin.ModelAdmin):
    list_display = ("user", "month", "total_salary")
    list_filter = ("month",)
