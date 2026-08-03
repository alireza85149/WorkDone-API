from django.db import models
from apps.contracts.models import Contract

class Submission(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REVISION = "revision", "Needs Revision"

    contract = models.ForeignKey(
        Contract,
        on_delete=models.CASCADE,
        related_name="submissions"
    )

    message = models.TextField()

    attachment = models.FileField(
        upload_to="submissions/",
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    submitted_at = models.DateTimeField(
        auto_now_add=True
    )