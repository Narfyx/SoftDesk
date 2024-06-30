from django.urls import path

from .views import (
    CommentCreate,
    CommentDetail,
    CommentViewSet,
    ContributorIndexViewSet,
    IssueDetail,
    IssueListCreate,
    IssueViewSet,
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
    path("issue/create/", IssueListCreate.as_view(), name="issue-list-create"),
    path("issue/all/", IssueViewSet.as_view({"get": "list"}), name="issue-all"),
    path("issue/<int:issue_pk>/", IssueDetail.as_view(), name="issue-detail"),
    path("comment/create/", CommentCreate.as_view(), name="comment-create"),
    path(
        "comment/<int:comment_pk>/",
        CommentDetail.as_view(),
        name="comment-detail",
    ),
    path(
        "comment/all/",
        CommentViewSet.as_view({"get": "list"}),
        name="comment-list",
    ),
]
