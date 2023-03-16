from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models.aggregates import Avg

from rest_framework import mixins, viewsets, filters
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .filters import TitlesFilter
from reviews.models import Category, Comment, User, Genre, Review, Titles
from .permissions import IsAdmin, IsAdminModeratorOwnerOrReadOnly, IsAdminOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleSerializer,
                          )


class CustomMixin(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    pass


class CategoryViewSet(CustomMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    # permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CustomMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter]
    # permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    search_fields = ('name', )
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all().annotate(rating=Avg('review__score'))
    # permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitlesFilter
    filterset_fields = ('name', )

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleSerializer
        return TitleSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        IsAdminModeratorOwnerOrReadOnly,
        IsAuthenticatedOrReadOnly
    )

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        title = get_object_or_404(Titles, pk=title_id)
        review = get_object_or_404(Review, pk=review_id)
        return Comment.objects.filter(title=title, review=review).all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        title = get_object_or_404(Titles, pk=title_id)
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user, title=title, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    # permission_classes = (
    #     IsAdminModeratorOwnerOrReadOnly,
    #     IsAuthenticatedOrReadOnly
    # )
    def get_title(self):
        return get_object_or_404(
            Titles,
            id=self.kwargs.get('title_id')
        )
        
    def get_queryset(self):
        return self.get_title().reviews.all()

    # def get_queryset(self):
    #     title_id = self.kwargs.get('title_id')
    #     title = get_object_or_404(Titles, pk=title_id)
    #     return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, pk=title_id)
        user = self.request.user
        serializer.save(author=user, title=title)
