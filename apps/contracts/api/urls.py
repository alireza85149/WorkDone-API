from django.urls import path
from .views import CompleteContractView, CnacelContractView

urlpatterns = [
    path('contracts/<int:pk>/complete/', CompleteContractView.as_view()),
    path('contracts/<int:pk>/cnacel/', CnacelContractView.as_view()),
]