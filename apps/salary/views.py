from datetime import date

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import SalaryRecord
from .services import calculate_monthly_salary
from core.permissions.base import IsCEO
from apps.users.models import User


class CalculateSalaryView(APIView):
    """Faqat CEO chaqira oladi - berilgan xodim va oy uchun oylikni hisoblaydi."""

    permission_classes = [IsAuthenticated, IsCEO]

    def post(self, request, user_id, year, month):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "Foydalanuvchi topilmadi"}, status=404)

        record = calculate_monthly_salary(user, date(year=year, month=month, day=1))
        return Response(
            {
                "user": user.get_full_name() or user.username,
                "month": record.month,
                "base_salary": record.base_salary,
                "total_bonus": record.total_bonus,
                "total_salary": record.total_salary,
            }
        )


class MySalaryView(APIView):
    """Har bir xodim faqat o'z oylik tarixini ko'radi."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        records = SalaryRecord.objects.filter(user=request.user).order_by("-month")
        data = [
            {
                "month": r.month,
                "base_salary": r.base_salary,
                "total_bonus": r.total_bonus,
                "total_salary": r.total_salary,
            }
            for r in records
        ]
        return Response(data)
