from rest_framework import serializers
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    progress_percent = serializers.ReadOnlyField()

    class Meta:
        model = Project
        fields = [
            "id", "title", "description", "client", "pm",
            "status", "created_by", "created_at", "progress_percent",
        ]
        read_only_fields = ["created_by", "created_at"]


class ProjectClientSerializer(serializers.ModelSerializer):
    """Mijoz uchun - faqat umumiy progress, ichki tafsilotlarsiz."""
    progress_percent = serializers.ReadOnlyField()

    class Meta:
        model = Project
        fields = ["id", "title", "status", "progress_percent"]
