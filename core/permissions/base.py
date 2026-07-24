from rest_framework.permissions import BasePermission


class IsCEO(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == "ceo")


class IsPM(BasePermission):
    """CEO ham PM'ga tegishli amallarni bajara oladi."""

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and request.user.role in ("ceo", "pm")
        )


class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == "employee")


class IsClient(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == "client")
