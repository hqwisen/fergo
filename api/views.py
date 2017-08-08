from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Project


class ListProjects(APIView):

    def get(self, request, format=None):
        projects = [project.name for project in Project.objects.all()]
        return Response(projects)