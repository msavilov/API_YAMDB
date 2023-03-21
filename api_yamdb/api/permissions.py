from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrReadOnly(BasePermission):
    """
    Создавать могут только авторизованные пользователи.
    Изменять может только автор, модератор или администратор.
    """
    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS
                    or request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if request.user == obj.author:
            return True

        if request.user.is_moderator or request.user.is_admin:
            return True

        return False


class IsAdminOrReadOnly(BasePermission):
    """
    Изменять может только администратор.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if (request.user and request.user.is_authenticated
           and request.user.is_admin):
            return True

        return False


class IsAdminUser(BasePermission):
    """
    Разрешает доступ только пользователям с правами администратора.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated
                    and request.user.is_admin)
