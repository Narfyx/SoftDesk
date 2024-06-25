from rest_framework import permissions

from projects.models import Contributor, Project

from .models import Issue


class IsIssueContributor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # obj here is an Issue instance
        return Contributor.objects.filter(
            user=request.user, project=obj.project
        ).exists()
