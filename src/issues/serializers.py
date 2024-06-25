from rest_framework import serializers

from projects.models import Contributor, Project

from .models import Comment, Issue


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = [
            "id",
            "title",
            "description",
            "priority",
            "tag",
            "status",
            "project",
            "author",
            "assignee",
        ]
        read_only_fields = ["author"]

    def validate(self, data):
        # Ensure the assignee is a contributor of the project
        project = data.get("project")
        assignee = data.get("assignee")
        if (
            assignee
            and not Contributor.objects.filter(user=assignee, project=project).exists()
        ):
            raise serializers.ValidationError(
                "The assignee must be a contributor of the project."
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "issue", "author", "body"]


class CommentDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = "__all__"
