from rest_framework import generics, permissions, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Contributor, Project
from .permissions import ContributorPermission
from .serializers import ContributorSerializer, ProjectSerializer


class ProjectCreate(generics.CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectIndexViewSet(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        project = Project.objects.get(pk=pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def put(self, request, pk):
        project = Project.objects.get(pk=pk)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=204)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
            project.delete()
            return Response(status=204)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=404)


class ContributorIndexViewSet(APIView):
    permission_classes = [IsAuthenticated, ContributorPermission]

    def put(self, request):
        serializer = ContributorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request):
        user_id = request.data.get("user")
        project_id = request.data.get("project")

        if user_id is None or project_id is None:
            return Response(
                {"error": "User ID and Project ID are required"},
                status=400,
            )

        try:
            contributor = Contributor.objects.get(
                user_id=user_id, project_id=project_id
            )
            contributor.delete()
            return Response(status=204)
        except Contributor.DoesNotExist:
            return Response({"error": "Contributor not found"}, status=404)
