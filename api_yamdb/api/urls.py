from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    GetTokenView,
    RegistrationView,
    ReviewViewSet,
    TitlesViewSet,
    UserViewSet,
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'genres', GenreViewSet, basename='genre')
router.register(r'titles', TitlesViewSet, basename='titles')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                r'/comments', CommentViewSet, basename='comments')


urlpatterns_auth = [
    path('signup/', RegistrationView.as_view(), name='signup'),
    path('token/', GetTokenView.as_view(), name='get_token'),
]


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/', include(urlpatterns_auth)),
]
