from rest_framework import permissions


class IsReviewOwner(permissions.BasePermission):
    """
    Only the reviewer may update or delete their review.
    Read-only access granted to authenticated users (or you can tighten as needed).
    """

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS (GET, HEAD, OPTIONS) allowed for authenticated users via global settings.
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.reviewer == request.user
