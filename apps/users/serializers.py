from rest_framework import serializers
from .models import User, Permission, UserPermission


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["id", "code", "name"]


class UserSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id", "username", "first_name", "last_name",
            "phone", "telegram_id", "role", "is_active_employee",
            "permissions",
        ]
        read_only_fields = ["telegram_id"]

    def get_permissions(self, obj):
        return list(
            UserPermission.objects.filter(user=obj).values_list("permission__code", flat=True)
        )
