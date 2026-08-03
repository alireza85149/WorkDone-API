from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from apps.notifications.models import Notification
from apps.notifications.api.serializers import NotificationSerializer
from apps.notifications.api.permissions import IsAuthenticatedOnly, IsNotificationOwner


class NotificationListView(generics.ListAPIView):
    """List notifications for the authenticated user."""
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticatedOnly]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


class NotificationRetrieveView(generics.RetrieveAPIView):
    """Retrieve a single notification (owner only)."""
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    permission_classes = [IsAuthenticatedOnly, IsNotificationOwner]


class MarkNotificationAsReadView(generics.UpdateAPIView):
    """Mark a notification as read. Returns the updated notification."""
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    permission_classes = [IsAuthenticatedOnly, IsNotificationOwner]

    def patch(self, request, *args, **kwargs):
        notification = self.get_object()
        if notification.is_read:
            return Response(self.get_serializer(notification).data)
        notification.is_read = True
        notification.save(update_fields=["is_read"])
        return Response(self.get_serializer(notification).data)
