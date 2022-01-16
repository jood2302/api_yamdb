from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Доступ на чтение для всех.
    На изменение -  для админа."""

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == 'admin':
            return True

        elif request.method in permissions.SAFE_METHODS:
            return True


class IsUserOrAdminOrModerOrReadOnly(permissions.BasePermission):
    """Доступ на чтение для всех.
    На изменение -  для автора, либо админа и модератора"""
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user
                or request.user.role in ('admin', 'moderator'))
