from django.urls import path

from .views import (
    ContributorIndexViewSet,
    ProjectCreate,
    ProjectIndexViewSet,
    ProjectViewSet,
)

urlpatterns = [
    path("create/", ProjectCreate.as_view(), name="project-create"),
    path(
        "all/",
        ProjectViewSet.as_view({"get": "list"}),
        name="project-list",
    ),
    path("<int:pk>/", ProjectIndexViewSet.as_view(), name="project"),
    path(
        "contributors/",
        ContributorIndexViewSet.as_view(),
        name="project-contributors",
    ),
]
