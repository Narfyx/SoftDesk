from rest_framework import serializers

from users.models import User

from .models import Comment, Contributor, Issue, Project


class ProjectSerializer(serializers.ModelSerializer):
    contributors = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True, required=False
    )

    class Meta:
        model = Project
        fields = ["id", "name", "description", "type_project", "author", "contributors"]
        read_only_fields = ["author"]


class ContributorSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Contributor
        fields = ("id", "user", "project")


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
