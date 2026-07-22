from django.urls import path
from .views import ProposalCreateView , ProposalCheckView, ProposalAcceptOrRejectView
urlpatterns = [
    path('project/<int:project_id>/proposal_create/', ProposalCreateView.as_view() ),
    path('project/<int:project_id>/proposal_check/', ProposalCheckView.as_view()),
    path('proposal_accept_or_denie/<int:pk>/', ProposalAcceptOrRejectView.as_view()),
]