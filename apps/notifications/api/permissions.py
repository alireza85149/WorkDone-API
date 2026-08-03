from rest_framework import permissions


class IsAuthenticatedOnly(permissions.BasePermission):
    """Allow access only to authenticated users."""

    def has_permission(self, request, view):
        return bool(request and request.user and request.user.is_authenticated)


class IsNotificationOwner(permissions.BasePermission):
    """Object-level permission to only allow owners of a notification to access it."""

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
