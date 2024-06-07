from rest_framework import serializers

from .models import Contributor, Project


class ProjectSerializer(serializers.ModelSerializer):
    # contributors = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ["id", "name", "description", "type_project", "author"]


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ("id", "user", "project")
