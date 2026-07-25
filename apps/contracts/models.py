from django.db import models
from apps.projects.models import Project
from apps.proposals.models import Proposal
from apps.accounts.models import EmployerProfile, FreelancerProfile
class Contract(models.Model):

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    project = models.OneToOneField(
        Project,
        on_delete=models.CASCADE,
        related_name="contract"
    )

    proposal = models.OneToOneField(
        Proposal,
        on_delete=models.CASCADE,
        related_name="contract"
    )

    employer = models.ForeignKey(
        EmployerProfile,
        on_delete=models.CASCADE
    )

    freelancer = models.ForeignKey(
        FreelancerProfile,
        on_delete=models.CASCADE
    )

    agreed_budget = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    deadline = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE
    )

    created_at = models.DateTimeField(auto_now_add=True)