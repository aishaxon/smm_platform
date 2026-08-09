from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, PermissionViewSet, ClientRegisterView

router = DefaultRouter()
router.register("employees", UserViewSet, basename="employee")
router.register("permissions", PermissionViewSet, basename="permission")

urlpatterns = [
    path("register/", ClientRegisterView.as_view(), name="client-register"),
] + router.urls