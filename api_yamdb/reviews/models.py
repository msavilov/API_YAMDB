from datetime import datetime

from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator,
)
from django.db import models

from users.models import User

MIN_SCORE = 1
MAX_SCORE = 10
DEFAULT_SCORE = 10


class CategoriesGenresAbstract(models.Model):
    """Абстрактная модель для жанров и категории"""

    name = models.CharField(
        'Название',
        max_length=256,
    )

    slug = models.SlugField(
        'Slug',
        max_length=50,
        unique=True,
        validators=[
            RegexValidator(
                regex='^[-a-zA-Z0-9_]+$'
            )
        ],
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Category(CategoriesGenresAbstract):
    """Модель категории"""

    class Meta(CategoriesGenresAbstract.Meta):
        ordering = ('slug',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(CategoriesGenresAbstract):
    """Модель жанра"""

    class Meta(CategoriesGenresAbstract.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Модель произведения"""

    name = models.CharField(
        verbose_name='Название',
        max_length=256,
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
        db_index=True,
        validators=(MaxValueValidator(int(datetime.now().year)),),
    )
    description = models.TextField(
        verbose_name='Описание',
        max_length=256,
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        default_related_name = 'titles'
        ordering = ('id',)

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель обзора и оценки произведения"""

    text = models.CharField(
        verbose_name='Текст отзыва',
        max_length=150,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации отзыва',
        auto_now_add=True,
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
    )
    score = models.IntegerField(
        verbose_name='Оценка',
        default=DEFAULT_SCORE,
        validators=(
            MinValueValidator(MIN_SCORE),
            MaxValueValidator(MAX_SCORE),
        ),
        error_messages={
            'validators': f'Score must be from {MIN_SCORE} to {MAX_SCORE}!'
        }
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'review'
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_autor',
            )
        ]

    def __str__(self):
        return f'Обзор {self.author} на {self.title}'


class Comment(models.Model):
    """Модель комментария к произведению"""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата комментария',
        auto_now_add=True,
        db_index=True,
    )
    text = models.TextField(
        verbose_name='Текст комментария'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
