from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Project
from .serializers import ProjectSerializer

class ProjectAPIView(APIView):

    def get(self, request, uuid):
        project = get_object_or_404(Project,
                                    pk = uuid)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)
