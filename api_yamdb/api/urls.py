from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    GetTokenView, RegistrationView, ReviewViewSet,
                    TitlesViewSet, UserViewSet)

v1_router = DefaultRouter()
v1_router.register(r'v1/categories', CategoryViewSet, basename='category')
v1_router.register(r'v1/genres', GenreViewSet, basename='genre')
v1_router.register(r'v1/titles', TitlesViewSet, basename='titles')
v1_router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
v1_router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                r'/comments', CommentViewSet, basename='comments')
v1_router.register(r'v1/user', UserViewSet, basename='user')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/', RegistrationView.as_view(), name='signup'),
    path('v1/auth/token/', GetTokenView.as_view(), name='get_token')
]
