from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Project(models.Model):
    PROJECT_TYPES = [
        ("BACK_END", "Back-end"),
        ("FRONT_END", "Front-end"),
        ("IOS", "iOS"),
        ("ANDROID", "Android"),
    ]

    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=8192)
    type_project = models.CharField(max_length=9, choices=PROJECT_TYPES)
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="authored_projects",
    )

    def __str__(self):
        return self.name
