from rest_framework import permissions

from .models import Project


class ContributorPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "DELETE":
            user_id = request.data.get("user")
            project_id = request.data.get("project")

            if user_id is None or project_id is None:
                return False

            try:
                project = Project.objects.get(id=project_id)
                return project.author == request.user
            except Project.DoesNotExist:
                return False
        return True
