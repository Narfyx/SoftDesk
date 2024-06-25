from django.urls import path

from .views import (
    CommentCreate,
    CommentDetail,
    IssueDetail,
    IssueListCreate,
    IssueViewSet,
)

urlpatterns = [
    path("create/", IssueListCreate.as_view(), name="issue-list-create"),
    path("all/", IssueViewSet.as_view({"get": "list"}), name="issue-all"),
    path("<int:issue_pk>/", IssueDetail.as_view(), name="issue-detail"),
    path("comment/create/", CommentCreate.as_view(), name="comment-create"),
    path(
        "comment/<int:comment_pk>/",
        CommentDetail.as_view(),
        name="comment-detail",
    ),
]
