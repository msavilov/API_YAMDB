from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comment, Genre, Review, Title, User


class GenreSerializer(serializers.ModelSerializer):
    """Серилизатор для жанров"""
    class Meta:
        model = Genre
        exclude = ('id',)


class CategorySerializer(serializers.ModelSerializer):
    """Серилизатор для категории"""
    class Meta:
        model = Category
        exclude = ('id',)


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitleCreateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        slug_field='slug',
        allow_empty=False,
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        exclude = ('title',)
        read_only_fields = (
            'id',
            'author',
            'pub_date',
        )

    def validate(self, data):
        if self.context['request'].method == 'POST':
            user = self.context['request'].user
            title_id = self.context['view'].kwargs.get('title_id')
            if Review.objects.filter(author=user, title_id=title_id).exists():
                raise serializers.ValidationError('Отзыв уже оставлен.')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        exclude = ('review',)
        read_only_fields = (
            'id',
            'author',
            'pub_date',
        )


class RegistrationSerializer(serializers.Serializer):
    """Сериализатор для регистрации"""
    email = serializers.EmailField(
        max_length=254,
        required=True,
    )
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[RegexValidator(regex=r'^[\w.@+-]+\Z'), ]
    )

    # class Meta:
    #     model = User
        # fields = (
        #     'username',
        #     'email',
        #     'first_name',
        #     'last_name',
        #     'bio',
        #     'role',
        # )

    def validate(self, value):
        print(value)
        username = value.get('username')
        email = value.get('email')

        if not email:
            return ValidationError(
                'Значение email не должно быть пустым.'
            )

        if not User.objects.filter(username=username).exists():
            if User.objects.filter(email=email).exists():
                raise ValidationError(
                    "Пользователь с email {email} уже существует."
                )

        return value

    def validate_username(self, value):
        if value == 'me':
            raise ValidationError(
                'Использовать имя "me" в качестве username запрещено.'
            )
        # if User.objects.filter(username=value).exists():
        #     raise ValidationError(
        #         f'Пользователь с username {value} уже существует.'
        #     )
        return value

    # def validate_email(self, value):
    #     if User.objects.filter(email=value).exists():
    #         raise ValidationError(
    #             f'Пользователь с email {value} уже существует.'
    #         )
    #     if value:
    #         return value
    #     raise ValidationError('Значение email не должно быть пустым.')


class GetTokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена"""
    username = serializers.CharField(
        max_length=150,
        required=True,
    )
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для user"""
    email = serializers.EmailField(
        max_length=254,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )