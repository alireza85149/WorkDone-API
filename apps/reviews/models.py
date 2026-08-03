from django.db import models
from apps.contracts.models import Contract
from apps.accounts.models import User


class Review(models.Model):
    """
    A review left by either the employer or freelancer for a completed contract.
    One review per contract per reviewer is enforced at the view/serializer level.
    """
    contract = models.ForeignKey(
        Contract, related_name="reviews", on_delete=models.CASCADE
    )
    reviewer = models.ForeignKey(
        User, related_name="reviews", on_delete=models.CASCADE
    )
    rating = models.PositiveSmallIntegerField(
        help_text="Integer rating between 1 and 5"
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["contract", "reviewer"]),
        ]

    def __str__(self):
        return f"Review({self.pk}) contract={self.contract_id} reviewer={self.reviewer_id} rating={self.rating}"
