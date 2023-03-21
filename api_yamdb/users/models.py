from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class Role(models.TextChoices):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        validators=[RegexValidator(regex=r'^[\w.@+-]+\Z'), ],
        unique=True,
    )
    email = models.EmailField(
        unique=True,
    )
    bio = models.TextField(blank=True)
    role = models.CharField(
        max_length=254,
        choices=Role.choices,
        default=Role.USER,
        blank=True,
    )

    @property
    def is_moderator(self):
        return self.role == Role.MODERATOR

    @property
    def is_admin(self):
        return self.role == Role.ADMIN or self.is_superuser
