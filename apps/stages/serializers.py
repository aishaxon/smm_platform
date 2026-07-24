from rest_framework import serializers
from .models import Stage, Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "stage", "title", "assigned_to", "is_done", "deadline", "completed_at"]


class StageSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Stage
        fields = [
            "id", "project", "title", "order_index", "assigned_to",
            "required_permission", "status", "started_at", "completed_at", "tasks",
        ]
        read_only_fields = ["started_at", "completed_at"]
