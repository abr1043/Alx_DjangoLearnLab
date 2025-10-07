from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission: allow safe methods for anyone, but only owners can edit/delete.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions only for the object's owner (author)
        return getattr(obj, 'author', None) == request.user
