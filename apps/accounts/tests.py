from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import (
    User,
    FreelancerProfile,
    EmployerProfile,
)


class RegistrationTests(APITestCase):

    def test_freelancer_can_register(self):
        data = {
            "email": "freelancer@example.com",
            "password": "StrongPassword123",
            "phone_number": "09123456789",
            "role": User.Role.FREELANCER,
        }

        response = self.client.post(
            reverse("register"),
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        user = User.objects.get(
            email="freelancer@example.com"
        )

        self.assertEqual(
            user.role,
            User.Role.FREELANCER,
        )

        self.assertTrue(
            FreelancerProfile.objects.filter(
                user=user
            ).exists()
        )

    def test_employer_can_register(self):
        data = {
            "email": "employer@example.com",
            "password": "StrongPassword123",
            "phone_number": "09123456788",
            "role": User.Role.EMPLOYER,
        }

        response = self.client.post(
            reverse("register"),
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        user = User.objects.get(
            email="employer@example.com"
        )

        self.assertEqual(
            user.role,
            User.Role.EMPLOYER,
        )

        self.assertTrue(
            EmployerProfile.objects.filter(
                user=user
            ).exists()
        )

    def test_duplicate_email_is_rejected(self):
        data = {
            "email": "duplicate@example.com",
            "password": "StrongPassword123",
            "phone_number": "09123456789",
            "role": User.Role.FREELANCER,
        }

        first_response = self.client.post(
            reverse("register"),
            data,
            format="json",
        )

        self.assertEqual(
            first_response.status_code,
            status.HTTP_201_CREATED,
        )

        second_response = self.client.post(
            reverse("register"),
            data,
            format="json",
        )

        self.assertEqual(
            second_response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_short_password_is_rejected(self):
        data = {
            "email": "short@example.com",
            "password": "123",
            "phone_number": "09123456789",
            "role": User.Role.FREELANCER,
        }

        response = self.client.post(
            reverse("register"),
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

class LoginTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="StrongPassword123",
            role=User.Role.FREELANCER,
        )

    def test_user_can_login(self):
        data = {
            "email": "test@example.com",
            "password": "StrongPassword123",
        }

        response = self.client.post(
            reverse("login"),
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_with_wrong_password_fails(self):
        data = {
            "email": "test@example.com",
            "password": "WrongPassword123",
        }

        response = self.client.post(
            reverse("login"),
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_login_with_unknown_email_fails(self):
        data = {
            "email": "unknown@example.com",
            "password": "StrongPassword123",
        }

        response = self.client.post(
            reverse("login"),
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

class MeTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="StrongPassword123",
            role=User.Role.FREELANCER,
        )

    def test_authenticated_user_can_access_me(self):
        response = self.client.post(
            reverse("login"),
            {
                "email": "test@example.com",
                "password": "StrongPassword123",
            },
            format="json",
        )

        access_token = response.data["access"]

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )

        response = self.client.get(
            reverse("me")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["email"],
            self.user.email,
        )

    def test_unauthenticated_user_cannot_access_me(self):
        response = self.client.get(
            reverse("me")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )