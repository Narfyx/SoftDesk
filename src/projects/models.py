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
    contributors = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL,
        through="Contributor",
        related_name="project_contributors",
    )

    def __str__(self):
        return self.name


class Contributor(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.user


@receiver(post_save, sender=Project)
def project_created(sender, instance, created, **kwargs):
    if created:  # Only add the author as a contributor if it's a new project
        Contributor.objects.create(user=instance.author, project=instance)
