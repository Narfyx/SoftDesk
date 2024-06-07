from rest_framework import generics, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Project  # , Contributor

# from .permissions import IsContributor
from .serializers import ProjectSerializer  # , ContributorSerializer


class ProjectCreate(generics.CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]  # [permissions.IsAuthenticated]
