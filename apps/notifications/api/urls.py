from django.urls import path
from apps.notifications.api.views import (
    NotificationListView,
    NotificationRetrieveView,
    MarkNotificationAsReadView,
)

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),
    path('<int:pk>/', NotificationRetrieveView.as_view(), name='notification-detail'),
    path('<int:pk>/read/', MarkNotificationAsReadView.as_view(), name='notification-mark-read'),
]
