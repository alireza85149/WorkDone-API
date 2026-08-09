from django.urls import path
from .consumers import NotificationConsumer
from .middleware import JWTAuthMiddleware

websocket_urlpatterns = [
    path(
        "ws/notifications/",
        JWTAuthMiddleware(
            NotificationConsumer.as_asgi()
        ),
    ),
]