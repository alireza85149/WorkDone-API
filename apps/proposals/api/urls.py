from django.urls import path
from .views import PropsalCreateView
urlpatterns = [
    path('project/<int:project_id>/proposal/', PropsalCreateView.as_view() ),
]