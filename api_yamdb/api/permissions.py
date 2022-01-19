from rest_framework import permissions

from reviews.utils import ADMIN, MODER


class IsAdminOrReadOnly(permissions.BasePermission):
    """Доступ на чтение для всех.
    На изменение -  для админа."""

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == ADMIN:
            return True

        elif request.method in permissions.SAFE_METHODS:
            return True


class IsUserOrAdminOrModerOrReadOnly(permissions.BasePermission):
    """Доступ на чтение для всех.
    На изменение -  для автора, либо админа и модератора"""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return obj.author == request.user or request.user.role in (
                ADMIN,
                MODER,
            )
        return request.method in permissions.SAFE_METHODS
