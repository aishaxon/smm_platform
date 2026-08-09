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

class ClientRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "phone", "password"]

    def validate_phone(self, value):
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("Bu telefon raqam allaqachon ro'yxatdan o'tgan")
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(
            username=validated_data["phone"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            phone=validated_data["phone"],
            role="client",
        )
        user.set_password(password)
        user.save()
        return user