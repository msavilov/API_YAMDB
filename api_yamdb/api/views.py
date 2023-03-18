from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models.aggregates import Avg
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
# from rest_framework.permissions import IsAuthenticatedOrReadOnly
from reviews.models import Category, Genre, Review, Titles, User

from .filters import TitlesFilter
# from .permissions import (
#     IsAdmin,
#     IsAdminModeratorOwnerOrReadOnly,
#     IsAdminOrReadOnly,
# )
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, RegistrationSerializer,
                          ReviewSerializer, TitleSerializer)


class CustomMixin(
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    pass


class CategoryViewSet(CustomMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [SearchFilter]
    # permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CustomMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [SearchFilter]
    # permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    search_fields = ('name',)
    lookup_field = 'slug'


class TitlesViewSet(ModelViewSet):
    queryset = Titles.objects.all().annotate(rating=Avg('review__score'))
    # permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitlesFilter
    filterset_fields = ('name',)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleSerializer
        return TitleSerializer


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    queryset = Review.objects.all()

    # permission_classes = (
    #     IsAdminModeratorOwnerOrReadOnly,
    #     IsAuthenticatedOrReadOnly
    # )

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, pk=title_id)
        return Review.objects.filter(title=title)

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, pk=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    # permission_classes = (
    #     IsAdminModeratorOwnerOrReadOnly,
    #     IsAuthenticatedOrReadOnly
    # )

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)


class RegistrationViewSet(APIView):
    http_method_names = ['post']
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user, _ = User.objects.get_or_create(
            username=serializer.validated_data.get('username'),
            email=serializer.validated_data.get('email'),
        )
        code = default_token_generator.make_token(user)
        send_mail(
            f'<h1>Код подтверждения {code}</h1>',
            f'''<h3>Подтвердите адрес электронной почты</h3>
             Ваш код подтверждения указан ниже.
             Введите его в открытом окне браузера,
             и мы поможем вам войти в систему.
             <h1>{code}</h1>''',
            'no-reply@yamdb.ru',
            [serializer.validated_data.get('email')],
            fail_silently=False,
        )
        return Response(serializer.data, status=200)
