from django.db import models

from apps.accounts.models import EmployerProfile, Skill


class Project(models.Model):

    class Status(models.TextChoices):
        OPEN = "open", "Open"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    employer = models.ForeignKey(
        EmployerProfile,
        on_delete=models.CASCADE,
        related_name="projects",
    )

    title = models.CharField(max_length=200)

    description = models.TextField()

    budget = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    deadline = models.DateField()

    required_skills = models.ManyToManyField(
        Skill,
        related_name="projects",
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN,
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    location = models.CharField(
        max_length=100,
        blank=True
    )

    is_remote = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title