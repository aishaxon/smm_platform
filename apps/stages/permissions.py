from rest_framework.permissions import BasePermission


class IsAssignedEmployee(BasePermission):
    """Faqat shu bosqichga tayinlangan xodim uni boshlashi/yakunlashi mumkin."""

    def has_object_permission(self, request, view, obj):
        return obj.assigned_to_id == request.user.id


class HasStagePermission(BasePermission):
    """Foydalanuvchida shu bosqich uchun kerakli ruxsat kodi bor-yo'qligini tekshiradi."""

    def has_object_permission(self, request, view, obj):
        if request.user.role == "ceo":
            return True
        return request.user.userpermission_set.filter(
            permission=obj.required_permission
        ).exists()
