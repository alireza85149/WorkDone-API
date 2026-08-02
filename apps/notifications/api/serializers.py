from rest_framework import serializers
from apps.notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    user_id = serializers.IntegerField(source="user.id", read_only=True)

    class Meta:
        model = Notification
        fields = ["id", "user", "user_id", "title", "message", "is_read", "created_at"]
        read_only_fields = ["id", "user", "user_id", "is_read", "created_at"]
