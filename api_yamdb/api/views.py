from http import HTTPStatus

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models.aggregates import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, Review, Title, User

from .filters import TitlesFilter
from .permissions import IsAdminOrReadOnly, IsAdminUser, IsAuthorOrReadOnly
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    GetTokenSerializer,
    RegistrationSerializer,
    ReviewSerializer,
    TitleCreateSerializer,
    TitleReadSerializer,
    UserSerializer,
)


class CustomMixin(
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    '''Создание кастомного миксина'''


class CategoryViewSet(CustomMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CustomMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    search_fields = ('name',)
    lookup_field = 'slug'


class TitlesViewSet(ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg('review__score'))
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter
    filterset_fields = ('name',)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleReadSerializer
        return TitleCreateSerializer


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthorOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(title=self.get_title(), author=self.request.user)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthorOrReadOnly,)

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            review=self.get_review(), author=self.request.user
        )


class RegistrationView(APIView):
    http_method_names = ('post',)
    serializer_class = RegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user, _ = User.objects.get_or_create(
                **serializer.validated_data
            )
        except IntegrityError:
            return Response(serializer.data, HTTPStatus.BAD_REQUEST)
        code = default_token_generator.make_token(user)
        send_mail(
            f'<h1>Код подтверждения {code}</h1>',
            f'''<h3>Подтвердите адрес электронной почты</h3>
            Ваш код подтверждения указан ниже.
            Введите его в открытом окне браузера,
            и мы поможем вам войти в систему.
            <h1>{code}</h1>''',
            settings.DEFAULT_FROM_EMAIL,
            [serializer.validated_data.get('email')],
            fail_silently=False,
        )
        return Response(serializer.data, HTTPStatus.OK)


class GetTokenView(APIView):
    http_method_names = ('post',)
    serializer_class = GetTokenSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        user = get_object_or_404(User, username=username)
        confirmation_code = serializer.validated_data.get(
            'confirmation_code'
        )
        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response({'token': str(token)}, HTTPStatus.OK)
        return Response(
            {'confirmation_code': 'Истек срок кода подтверждения'},
            HTTPStatus.BAD_REQUEST,
        )


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    http_method_names = ('get', 'post', 'patch', 'delete',)
    lookup_field = 'username'

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        self.kwargs['username'] = request.user.username
        if request.method == 'PATCH':
            return self.partial_update(request)
        return self.retrieve(request)

    def perform_update(self, serializer):
        if self.action == 'me':
            serializer.save(role=self.request.user.role)
        else:
            serializer.save()
