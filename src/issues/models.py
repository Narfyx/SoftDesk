from django.conf import settings
from django.db import models

from projects.models import Project


class Issue(models.Model):
    PRIORITY_CHOICES = [("LOW", "Low"), ("MEDIUM", "Medium"), ("HIGH", "High")]
    TAG_CHOICES = [("BUG", "Bug"), ("FEATURE", "Feature"), ("TASK", "Task")]
    STATUS_CHOICES = [
        ("TODO", "To Do"),
        ("IN_PROGRESS", "In Progress"),
        ("FINISHED", "Finished"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(max_length=8192)
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES, default="LOW")
    tag = models.CharField(max_length=7, choices=TAG_CHOICES, default="TASK")
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default="TODO")
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="issues"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_issues",
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="assigned_issues",
        null=True,
        blank=True,
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):

    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_comment",
    )
    created = models.DateTimeField(auto_now_add=True)
    body = models.CharField(max_length=4096)
