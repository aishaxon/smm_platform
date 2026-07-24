from rest_framework.routers import DefaultRouter
from .views import UserViewSet, PermissionViewSet

router = DefaultRouter()
router.register("employees", UserViewSet, basename="employee")
router.register("permissions", PermissionViewSet, basename="permission")

urlpatterns = router.urls
