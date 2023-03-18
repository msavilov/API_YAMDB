from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'

    ROLE_CHOICES = (
        (USER, 'Пользователь'),
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
    )
    email = models.EmailField(
        max_length=256,
        unique=True,
        blank=False,
        null=False
    )

    role = models.CharField(
        max_length=256,
        choices=ROLE_CHOICES,
        blank=True
    )
    bio = models.TextField(blank=True)

    REQUIRED_FIELDS = ('email', )