from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """
    Доступ только пользователям из группы «Модераторы».
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.groups.filter(name="Модераторы").exists()
        )


class IsOwner(BasePermission):
    """
    Доступ к объекту только его владельцу.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner_id == request.user.id