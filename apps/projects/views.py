from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Project
from .serializers import ProjectSerializer
from core.permissions.base import IsPM


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "ceo":
            return Project.objects.all()
        if user.role == "pm":
            return Project.objects.filter(pm=user)
        if user.role == "employee":
            return Project.objects.filter(stages__assigned_to=user).distinct()
        if user.role == "client":
            return Project.objects.filter(client=user)
        return Project.objects.none()

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return [IsAuthenticated(), IsPM()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
