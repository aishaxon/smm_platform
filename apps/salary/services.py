from .models import SalaryRule, SalaryRecord
from apps.stages.models import Stage


def calculate_monthly_salary(user, month_date):
    rule, _ = SalaryRule.objects.get_or_create(user=user)

    done_count = Stage.objects.filter(
        assigned_to=user,
        status="done",
        completed_at__year=month_date.year,
        completed_at__month=month_date.month,
    ).count()

    total_bonus = done_count * rule.bonus_per_stage
    total = rule.base_salary + total_bonus

    record, _ = SalaryRecord.objects.update_or_create(
        user=user,
        month=month_date.replace(day=1),
        defaults={
            "base_salary": rule.base_salary,
            "total_bonus": total_bonus,
            "total_salary": total,
        },
    )
    return record
