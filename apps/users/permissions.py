from rest_framework.permissions import BasePermission


class IsSelfOrCEO(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.role == "ceo" or obj == request.user
