from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import User, FreelancerProfile, EmployerProfile


class RegistrationTests(APITestCase):

    def test_freelancer_can_register(self):
        data = {
            "email": "freelancer@example.com",
            "password": "StrongPassword123",
            "phone_number": "09123456789",
            "role": "freelancer",
        }

        response = self.client.post(
            reverse("register"),
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(
            email="freelancer@example.com"
        )

        self.assertEqual(user.role, User.Role.FREELANCER)

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
            "role": "employer",
        }

        response = self.client.post(
            reverse("register"),
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(
            email="employer@example.com"
        )

        self.assertEqual(user.role, User.Role.EMPLOYER)

        self.assertTrue(
            EmployerProfile.objects.filter(
                user=user
            ).exists()
        )

    def test_password_is_hashed(self):
        data = {
            "email": "hash@example.com",
            "password": "StrongPassword123",
            "phone_number": "09123456787",
            "role": "freelancer",
        }

        response = self.client.post(
            reverse("register"),
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(
            email="hash@example.com"
        )

        self.assertNotEqual(
            user.password,
            "StrongPassword123"
        )

        self.assertTrue(
            user.check_password("StrongPassword123")
        )


class LoginTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="login@example.com",
            password="StrongPassword123",
            role=User.Role.FREELANCER,
        )

    def test_user_can_login(self):
        response = self.client.post(
            reverse("login"),
            {
                "email": "login@example.com",
                "password": "StrongPassword123",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_wrong_password_is_rejected(self):
        response = self.client.post(
            reverse("login"),
            {
                "email": "login@example.com",
                "password": "WrongPassword123",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )


class MeTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="me@example.com",
            password="StrongPassword123",
            role=User.Role.FREELANCER,
        )

    def test_unauthenticated_user_cannot_access_me(self):
        response = self.client.get(
            reverse("me")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_authenticated_user_can_access_me(self):
        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.get(
            reverse("me")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["email"],
            self.user.email
        )