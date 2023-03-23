from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrReadOnly(BasePermission):
    """
    Создавать могут только авторизованные пользователи.
    Изменять может только автор, модератор или администратор.
    """
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user == obj.author
                or request.user.is_moderator
                or request.user.is_admin)


class IsAdminOrReadOnly(BasePermission):
    """
    Изменять может только администратор.
    """
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or (request.user.is_authenticated and request.user.is_admin))


class IsAdminUser(BasePermission):
    """
    Разрешает доступ только пользователям с правами администратора.
    """
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin)
