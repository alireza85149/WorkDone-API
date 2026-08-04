from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.shortcuts import get_object_or_404

from apps.contracts.models import Contract
from apps.reviews.models import Review
from apps.reviews.api.serializers import ReviewSerializer
from apps.reviews.api.permissions import IsReviewOwner


class ContractReviewListCreateView(generics.ListCreateAPIView):
    """
    List reviews for a contract and allow a contract participant to create a review.
    URL: /api/reviews/contracts/<contract_id>/reviews/
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        contract = get_object_or_404(Contract, pk=self.kwargs["contract_id"])
        return contract.reviews.all()

    def perform_create(self, serializer):
        contract = get_object_or_404(Contract, pk=self.kwargs["contract_id"])

        # Only participants (employer or freelancer) may create a review
        user = self.request.user
        is_employer = hasattr(user, "employer_profile") and user.employer_profile == contract.employer
        is_freelancer = hasattr(user, "freelancer_profile") and user.freelancer_profile == contract.freelancer

        if not (is_employer or is_freelancer):
            raise PermissionDenied("Only contract participants can create reviews.")

        # Optionally enforce contract completed status
        if contract.status != Contract.Status.COMPLETED:
            raise ValidationError("Reviews can only be created for completed contracts.")

        # Prevent duplicate review by the same reviewer for the same contract
        if contract.reviews.filter(reviewer=user).exists():
            raise ValidationError("You have already submitted a review for this contract.")

        serializer.save(contract=contract, reviewer=user)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete an individual review.
    URL: /api/reviews/reviews/<pk>/
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsReviewOwner]
    queryset = Review.objects.all()
