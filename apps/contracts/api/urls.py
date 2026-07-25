from django.urls import path
from .views import CompleteContractView, CancelContractView, RetrieveContractView, ListContractView

urlpatterns = [
    path('contracts/<int:pk>/complete/', CompleteContractView.as_view()),
    path('contracts/<int:pk>/cnacel/', CancelContractView.as_view()),
    path('contracts/<int:pk>/', RetrieveContractView.as_view()),
    path('contracts/', ListContractView.as_view()),
]