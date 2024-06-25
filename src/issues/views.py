from rest_framework import generics, permissions, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from projects.models import Project

from .models import Comment, Issue
from .permissions import IsIssueContributor
from .serializers import CommentDetailSerializer, CommentSerializer, IssueSerializer


class IssueListCreate(generics.ListCreateAPIView):

    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated, IsIssueContributor]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer


class IssueDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, issue_pk):
        issue = Issue.objects.get(pk=issue_pk)
        serializer = IssueSerializer(issue)

        return Response(serializer.data)

    def put(self, request, issue_pk):
        issue = Issue.objects.get(pk=issue_pk)
        serializer = IssueSerializer(issue, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=204)
        return Response(serializer.errors, status=400)


class CommentCreate(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]  # [permissions.IsAuthenticated, IsIssueContributor]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        return Comment.objects.all()


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, comment_pk):
        comment = Comment.objects.get(pk=comment_pk)
        serializer = CommentSerializer(comment)

        return Response(serializer.data)

    def put(self, request, comment_pk):
        comment = Comment.objects.get(pk=comment_pk)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=204)
        return Response(serializer.errors, status=400)
