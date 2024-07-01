from rest_framework import generics, status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Comment, Contributor, Issue, Project
from .permissions import (
    IsCommentAuthorPermission,
    IsContributorPermission,
    IsIssueAuthorPermission,
    IsIssueContributorPermission,
    IsProjectAuthorPermission,
)
from .serializers import (
    CommentSerializer,
    ContributorSerializer,
    IssueSerializer,
    ProjectSerializer,
    ShowAllProjectsSerializer,
    ShowAllIssueSerializer,
    ShowAllCommentSerializer,
)


class ProjectCreate(generics.CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ShowAllProjectsSerializer
    permission_classes = [IsAuthenticated]


class ProjectIndexViewSet(APIView):
    permission_classes = [IsAuthenticated]  # Default for all methods

    def get_permissions(self):
        # Set specific permissions for each method
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            self.permission_classes = [IsProjectAuthorPermission]
        elif self.request.method == "GET":
            self.permission_classes = [IsContributorPermission]
        return super().get_permissions()

    def get(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise NotFound(detail="Project not found")

        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise NotFound(detail="Project not found")

        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise NotFound(detail="Project not found")

        serializer = ProjectSerializer(
            project, data=request.data, partial=True
        )  # Utilisation de `partial=True` pour les mises à jour partielles
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise NotFound(detail="Project not found")

        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContributorIndexViewSet(APIView):
    permission_classes = [IsAuthenticated]  # Default for all methods

    def get_permissions(self):
        # Set specific permissions for each method
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            self.permission_classes = [IsProjectAuthorPermission]
        elif self.request.method in ["GET"]:
            self.permission_classes = [IsContributorPermission]
        return super().get_permissions()

    def put(self, request):
        serializer = ContributorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user_id = request.data.get("user")
        project_id = request.data.get("project")

        if user_id is None or project_id is None:
            return Response(
                {"error": "User ID and Project ID are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            contributor = Contributor.objects.get(
                user_id=user_id, project_id=project_id
            )
            contributor.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Contributor.DoesNotExist:
            return Response(
                {"error": "Contributor not found"}, status=status.HTTP_404_NOT_FOUND
            )


class IssueListCreate(generics.ListCreateAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]  # Default for all methods

    def get_permissions(self):
        if self.request.method in ["POST"]:
            self.permission_classes = [IsContributorPermission]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = ShowAllIssueSerializer
    permission_classes = [IsAuthenticated]


class IssueDetail(APIView):
    permission_classes = [IsAuthenticated]  # Default for all methods

    def get_permissions(self):
        # Set specific permissions for each method
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            self.permission_classes = [IsIssueAuthorPermission]
        elif self.request.method in ["GET"]:
            self.permission_classes = [IsIssueContributorPermission]
        return super().get_permissions()

    def get(self, request, issue_pk):
        try:
            issue = Issue.objects.get(pk=issue_pk)
        except Issue.DoesNotExist:
            raise NotFound(detail="Issue not found")

        serializer = IssueSerializer(issue)
        return Response(serializer.data)

    def put(self, request, issue_pk):
        try:
            issue = Issue.objects.get(pk=issue_pk)
        except Issue.DoesNotExist:
            raise NotFound(detail="Issue not found")

        serializer = IssueSerializer(issue, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, issue_pk):
        try:
            issue = Issue.objects.get(pk=issue_pk)
        except Issue.DoesNotExist:
            raise NotFound(detail="Issue not found")

        serializer = IssueSerializer(
            issue, data=request.data, partial=True
        )  # Utilisation de `partial=True` pour les mises à jour partielles
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, issue_pk):
        try:
            issue = Issue.objects.get(pk=issue_pk)
        except Issue.DoesNotExist:
            raise NotFound(detail="Issue not found")

        self.check_object_permissions(request, issue)

        issue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentCreate(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]  # Default for all methods

    def initialize_request(self, request, *args, **kwargs):
        request = super().initialize_request(request, *args, **kwargs)

        if request.method == "POST":
            issue_id = request.data.get("issue")
            if issue_id:
                try:
                    issue = Issue.objects.get(id=issue_id)
                    mutable_data = (
                        request.data.copy()
                    )  # Créer une copie mutable des données
                    mutable_data["project"] = issue.project.id
                    mutable_data["author"] = request.user.id  # Ajouter l'ID de l'auteur
                    request._full_data = (
                        mutable_data  # Réassigner les données modifiées
                    )
                except Issue.DoesNotExist:
                    raise NotFound(detail="Issue not found")

        return request

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [IsContributorPermission]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = ShowAllCommentSerializer
    permission_classes = [IsAuthenticated]


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        # Set specific permissions for each method
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            self.permission_classes = [IsCommentAuthorPermission]
        elif self.request.method in ["GET"]:
            self.permission_classes = [IsIssueContributorPermission]
        return super().get_permissions()

    def get(self, request, comment_pk):
        try:
            comment = Comment.objects.get(pk=comment_pk)
        except Comment.DoesNotExist:
            raise NotFound(detail="Comment not found")

        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def put(self, request, comment_pk):
        try:
            comment = Comment.objects.get(pk=comment_pk)
        except Comment.DoesNotExist:
            raise NotFound(detail="Comment not found")

        self.check_object_permissions(request, comment)

        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, comment_pk):
        try:
            comment = Comment.objects.get(pk=comment_pk)
        except Comment.DoesNotExist:
            raise NotFound(detail="Comment not found")

        self.check_object_permissions(request, comment)

        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_pk):
        try:
            comment = Comment.objects.get(pk=comment_pk)
        except Comment.DoesNotExist:
            raise NotFound(detail="Comment not found")

        self.check_object_permissions(request, comment)

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
