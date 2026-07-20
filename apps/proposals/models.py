from django.db import models
from apps.accounts.models import FreelancerProfile
from apps.projects.models import Project
# Create your models here.
class Proposal(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        ACCEPTED = 'accepted', 'Accepted'
        REJECTED = 'rejected', 'Rejcted'

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="proposals"
    )

    freelancer = models.ForeignKey(
        FreelancerProfile,
        on_delete=models.CASCADE,
        related_name="proposals"
    )

    cover_letter = models.TextField()

    proposed_budget = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    estimated_days = models.PositiveIntegerField()

    status = models.CharField(
        choices=Status.choices,
        default=Status.PENDING,
        max_length=20
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )