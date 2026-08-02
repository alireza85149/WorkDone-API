from django.urls import path
from apps.reviews.api.views import ContractReviewListCreateView, ReviewDetailView

urlpatterns = [
    path("contracts/<int:contract_id>/reviews/", ContractReviewListCreateView.as_view(), name="contract-reviews"),
    path("reviews/<int:pk>/", ReviewDetailView.as_view(), name="review-detail"),
]
