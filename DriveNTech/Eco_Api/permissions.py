from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit objects.
    Non-admin users can only read.
    """

    def has_permission(self, request, view, obj):
        # Allow read-only access for non-authenticated users
        if request.method in permissions.SAFE_METHODS:
            return True
        # this is the custom permission class that allows only admins to edit objects, while non-admin users can only read them.
        return obj.owner == request.user


