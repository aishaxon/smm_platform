from rest_framework.permissions import BasePermission


class IsAssignedEmployee(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.assigned_to_id == request.user.id


class HasStagePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == "ceo":
            return True
        return request.user.userpermission_set.filter(
            permission=obj.required_permission
        ).exists()
