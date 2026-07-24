from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.projects.models import Project
from apps.projects.serializers import ProjectClientSerializer
from core.permissions.base import IsClient


class MyProjectsView(APIView):
    permission_classes = [IsAuthenticated, IsClient]

    def get(self, request):
        projects = Project.objects.filter(client=request.user)
        return Response(ProjectClientSerializer(projects, many=True).data)
