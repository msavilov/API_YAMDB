from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.TextChoices):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'


class User(AbstractUser):
    bio = models.TextField(
        blank=True,
        verbose_name='Информация о пользователе',
    )
    role = models.CharField(
        max_length=254,
        choices=Role.choices,
        default=Role.USER,
        blank=True,
        verbose_name='Тип учётной записи',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_moderator(self):
        return self.role == Role.MODERATOR

    @property
    def is_admin(self):
        return self.role == Role.ADMIN or self.is_superuser
