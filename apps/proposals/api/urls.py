from django.urls import path
from .views import ProposalCreateView , ProposalCheckView, ProposalAcceptOrRejectView
urlpatterns = [
    path('project/<int:project_id>/proposal_create/', ProposalCreateView.as_view(), name='proposal-create'),
    path('project/<int:project_id>/proposal_check/', ProposalCheckView.as_view(), name='proposal-check'),
    path('proposal_accept_or_deny/<int:pk>/', ProposalAcceptOrRejectView.as_view(), name='proposal-accept-or-deny'),
]