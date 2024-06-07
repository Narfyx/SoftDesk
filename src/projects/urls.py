from django.urls import path

from .views import ContributorViewSet, ProjectCreate, ProjectViewSet

urlpatterns = [
    path("create/", ProjectCreate.as_view(), name="project-create"),
    path("projects/", ProjectViewSet.as_view({"get": "list"}), name="project-list"),
    path(
        "contributors/",
        ContributorViewSet.as_view({"get": "list"}),
        name="contributors-list",
    ),
]
