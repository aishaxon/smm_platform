from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Stage
from .serializers import StageSerializer
from .permissions import IsAssignedEmployee
from apps.notifications.services import notify_user


class StageViewSet(viewsets.ModelViewSet):
    serializer_class = StageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "ceo":
            return Stage.objects.all()
        if user.role == "pm":
            return Stage.objects.filter(project__pm=user)
        if user.role == "employee":
            return Stage.objects.filter(assigned_to=user)
        if user.role == "client":
            return Stage.objects.filter(project__client=user)
        return Stage.objects.none()

    def perform_create(self, serializer):
        stage = serializer.save()
        if stage.assigned_to_id:
            notify_user(stage.assigned_to_id, f"Sizga yangi bosqich tayinlandi: {stage.title}", "stage_assigned")

    def perform_update(self, serializer):
        old_assigned_id = self.get_object().assigned_to_id
        stage = serializer.save()
        if stage.assigned_to_id and stage.assigned_to_id != old_assigned_id:
            notify_user(stage.assigned_to_id, f"Sizga yangi bosqich tayinlandi: {stage.title}", "stage_assigned")

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated, IsAssignedEmployee])
    def start(self, request, pk=None):
        stage = self.get_object()
        stage.status = "in_progress"
        stage.started_at = timezone.now()
        stage.save(update_fields=["status", "started_at"])
        return Response(StageSerializer(stage).data)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated, IsAssignedEmployee])
    def complete(self, request, pk=None):
        stage = self.get_object()
        stage.mark_done()

        notify_user(stage.assigned_to_id, f"'{stage.title}' bosqichi yakunlandi", "stage_done")
        if stage.project.pm_id:
            notify_user(
                stage.project.pm_id,
                f"'{stage.title}' bosqichi ({stage.project.title}) yakunlandi",
                "stage_done",
            )
        return Response(StageSerializer(stage).data, status=status.HTTP_200_OK)
