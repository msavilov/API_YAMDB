from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comment, Genre, Review, Titles, User


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Titles
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date',
        )
        read_only_fields = (
            'id',
            'author',
            'pub_date',
        )
        model = Review
    
    # def validate(self, data):
    #     if self.context['request'].method == 'POST':
    #         user = self.context['request'].user
    #         title_id = self.context['view'].kwargs.get('title_id')
    #         if Review.objects.filter(author=user, title_id=title_id).exists():
    #             raise serializers.ValidationError('Отзыв уже оставлен.')
    #     return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
        )
        read_only_fields = (
            'id',
            'author',
            'pub_date',
        )
        model = Comment
