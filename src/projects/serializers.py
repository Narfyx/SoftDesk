from rest_framework import serializers

from users.models import User

from .models import Contributor, Project


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
