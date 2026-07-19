from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):

    class Role(models.TextChoices):
        FREELANCER = "freelancer", "Freelancer"
        EMPLOYER = "employer", "Employer"
        ADMIN = "admin", "Admin"

    email = models.EmailField(
        unique=True
    )

    role = models.CharField(
        max_length=20,
        choices=Role.choices
    )

    is_active = models.BooleanField(
        default=True
    )

    is_staff = models.BooleanField(
        default=False
    )

    is_verified = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    objects = UserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
class FreelancerProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="freelancer_profile",
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    bio = models.TextField(blank=True)

    skills = models.TextField(
        blank=True,
        help_text="Comma separated skills"
    )

    hourly_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    portfolio = models.URLField(blank=True)

    avatar = models.ImageField(
        upload_to="avatars/freelancers/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.email
    
class EmployerProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="employer_profile",
    )

    company_name = models.CharField(max_length=255)

    company_description = models.TextField(
        blank=True
    )

    website = models.URLField(blank=True)

    logo = models.ImageField(
        upload_to="logos/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.company_name