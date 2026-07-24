from django.urls import path
from .views import CalculateSalaryView, MySalaryView

urlpatterns = [
    path("calculate/<int:user_id>/<int:year>/<int:month>/", CalculateSalaryView.as_view(), name="calculate-salary"),
    path("my/", MySalaryView.as_view(), name="my-salary"),
]
