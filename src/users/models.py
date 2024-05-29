from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class User(AbstractUser):

    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    email = models.EmailField(max_length=254)
    age = models.PositiveIntegerField()
    can_be_contacted = models.BooleanField(
        default=False
    )  # (peut être contacté) : oui ou non
    can_data_be_shared = models.BooleanField(
        default=False
    )  # (peut-on partager les données) : oui ou non

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",  # Nom de relation unique
        blank=True,
        help_text=(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions_set",  # Nom de relation unique
        blank=True,
        help_text=("Specific permissions for this user."),
        related_query_name="user",
    )
