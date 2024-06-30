from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from .models import Comment, Contributor, Issue, Project


class IsContributorPermission(IsAuthenticated):
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            print(f"Utilisateur authentifié : {request.user}")

            if request.method == "GET":
                user_id = request.user.id
                project_id = view.kwargs.get("pk")  # Utiliser l'ID du projet de l'URL

                print(
                    f"Requête GET détectée. user_id : {user_id}, project_id : {project_id}"
                )

                if project_id is None:
                    print("project_id manquant")
                    return False

                try:
                    project = Project.objects.get(id=project_id)
                    is_author = project.author == request.user
                    is_contributor = Contributor.objects.filter(
                        user=request.user, project=project
                    ).exists()
                    print(
                        f"Projet trouvé. Utilisateur est auteur : {is_author}, Utilisateur est contributeur : {is_contributor}"
                    )
                    return is_author or is_contributor
                except Project.DoesNotExist:
                    print("Projet non trouvé")
                    return False
            elif request.method == "POST":
                user_id = request.user.id
                project_id = request.data.get("project")
                print(
                    f"Requête POST détectée. user_id : {user_id}, project_id : {project_id}"
                )
                if project_id is None:
                    print("project_id manquant")
                    return False
                try:
                    project = Project.objects.get(id=project_id)
                    is_contributor = Contributor.objects.filter(
                        user=request.user, project=project
                    ).exists()

                    return is_contributor
                except Project.DoesNotExist:
                    print("Projet non trouvé")
                    return False

            return True
        else:
            print("Utilisateur non authentifié")
            return False


class IsIssueAuthorPermission(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            print("Utilisateur non authentifié")
            return False

        if request.method not in ["PUT", "PATCH", "DELETE"]:
            print(f"Requête non autorisée: {request.method}")
            return False

        issue_id = view.kwargs.get("issue_pk")
        if issue_id is None:
            print("Issue ID manquant")
            return False

        try:
            issue = Issue.objects.get(id=issue_id)
            is_author = issue.author == request.user
            print(f"Utilisateur est auteur: {is_author}")
            return is_author
        except Issue.DoesNotExist:
            print("Issue non trouvée")
            return False


class IsIssueContributorPermission(IsAuthenticated):
    def has_permission(self, request, view):
        # Vérification d'authentification de base
        if not super().has_permission(request, view):
            print("Utilisateur non authentifié")
            return False

        # Autoriser seulement les requêtes GET
        if request.method in ["GET"]:
            issue_id = view.kwargs.get("issue_pk")
            if issue_id is None:
                print("Issue ID manquant")
                return False

            try:
                issue = Issue.objects.get(pk=issue_id)
                is_contributor = Contributor.objects.filter(
                    user=request.user, project=issue.project
                ).exists()
                print(f"Utilisateur est contributeur : {is_contributor}")
                return is_contributor
            except Issue.DoesNotExist:
                print("Issue non trouvée")
                return False
        print(f"Requête non autorisée : {request.method}")
        return False


class IsProjectAuthorPermission(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            print("Utilisateur non authentifié")
            return False

        if request.method not in ["PUT", "PATCH", "DELETE"]:
            print(f"Requête non autorisée: {request.method}")
            return False

        project_id = view.kwargs.get("pk") or request.data.get("project")
        if project_id is None:
            print("Project ID manquant")
            return False

        try:
            project = Project.objects.get(id=project_id)
            if request.method == "DELETE":
                user_id = request.data.get("user")
                if user_id is None:
                    print("User ID manquant pour DELETE")
                    return False

                # Autoriser si l'utilisateur souhaite se supprimer lui-même
                if request.user.id == int(user_id):
                    is_contributor = Contributor.objects.filter(
                        user=request.user, project=project
                    ).exists()
                    print(f"Utilisateur est contributeur: {is_contributor}")
                    return is_contributor

            is_author = project.author == request.user
            print(f"Utilisateur est auteur: {is_author}")
            return is_author
        except Project.DoesNotExist:
            print("Projet non trouvé")
            return False


class IsCommentAuthorPermission(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            print("Utilisateur non authentifié")
            return False

        if request.method not in ["PUT", "PATCH", "DELETE"]:
            print(f"Requête non autorisée: {request.method}")
            return False

        comment_id = view.kwargs.get("comment_pk")
        if comment_id is None:
            print("Comment ID manquant")
            return False

        try:
            comment = Comment.objects.get(id=comment_id)
            is_author = comment.author == request.user
            print(f"Utilisateur est auteur: {is_author}")
            return is_author
        except Comment.DoesNotExist:
            print("Commentaire non trouvé")
            return False
