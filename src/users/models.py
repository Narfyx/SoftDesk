from datetime import date

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.exceptions import ValidationError
from django.db import models


def validate_age(value):
    today = date.today()
    age = (
        today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    )
    if age < 15:
        raise ValidationError("User must be at least 15 years old.")


class User(AbstractUser):
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    birth_date = models.DateField(validators=[validate_age])
    email = models.EmailField(max_length=255, blank=False)

    def __str__(self):
        return self.username
