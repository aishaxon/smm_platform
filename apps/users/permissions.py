from rest_framework.permissions import BasePermission


class IsSelfOrCEO(BasePermission):
    """Foydalanuvchi faqat o'z profilini ko'radi/tahrirlaydi, CEO esa hammasini."""

    def has_object_permission(self, request, view, obj):
        return request.user.role == "ceo" or obj == request.user
