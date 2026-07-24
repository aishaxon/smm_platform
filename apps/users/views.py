import secrets
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import User, Permission, UserPermission
from .serializers import UserSerializer, PermissionSerializer
from core.permissions.base import IsCEO


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsCEO]

    def get_queryset(self):
        return User.objects.all().order_by("-created_at")

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def me(self, request):
        return Response(UserSerializer(request.user).data)

    @action(detail=False, methods=["post"])
    def create_employee(self, request):
        data = request.data
        phone = data.get("phone")
        if not phone:
            return Response({"error": "phone majburiy"}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(phone=phone).exists():
            return Response({"error": "Bu raqam allaqachon ro'yxatdan o'tgan"}, status=status.HTTP_400_BAD_REQUEST)

        raw_password = secrets.token_urlsafe(6)
        user = User.objects.create(
            username=phone,
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
            phone=phone,
            role=data.get("role", "employee"),
            password=make_password(raw_password),
        )

        for code in data.get("permission_codes", []):
            perm, _ = Permission.objects.get_or_create(code=code, defaults={"name": code})
            UserPermission.objects.get_or_create(user=user, permission=perm)

        return Response(
            {
                "user": UserSerializer(user).data,
                "generated_password": raw_password,
            },
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=["post"])
    def set_permissions(self, request, pk=None):
        user = self.get_object()
        codes = request.data.get("permission_codes", [])
        UserPermission.objects.filter(user=user).delete()
        for code in codes:
            perm, _ = Permission.objects.get_or_create(code=code, defaults={"name": code})
            UserPermission.objects.create(user=user, permission=perm)
        return Response(UserSerializer(user).data)


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated, IsCEO]
