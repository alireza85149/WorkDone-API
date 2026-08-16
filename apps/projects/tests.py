from datetime import date, timedelta

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import User
from apps.projects.models import Project


class ProjectTests(APITestCase):

    def setUp(self):
        # Employer
        self.employer = User.objects.create_user(
            email="employer@example.com",
            password="StrongPassword123",
            role=User.Role.EMPLOYER,
        )

        # Freelancer
        self.freelancer = User.objects.create_user(
            email="freelancer@example.com",
            password="StrongPassword123",
            role=User.Role.FREELANCER,
        )

        # Project owned by employer
        self.project = Project.objects.create(
            employer=self.employer.employer_profile,
            title="Build a REST API",
            description="Create a Django REST API.",
            budget=1000,
            deadline=date.today() + timedelta(days=30),
        )

        self.project_list_url = reverse("project-list")

        self.project_detail_url = reverse(
            "project-detail",
            kwargs={"pk": self.project.pk},
        )

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def test_authenticated_user_can_list_projects(self):
        self.authenticate(self.freelancer)

        response = self.client.get(self.project_list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_employer_can_create_project(self):
        self.authenticate(self.employer)

        data = {
            "title": "Build a Django Website",
            "description": "Create a professional website.",
            "budget": "1500.00",
            "deadline": str(
                date.today() + timedelta(days=30)
            ),
            "is_remote": True,
            "location": "",
        }

        response = self.client.post(
            self.project_list_url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            Project.objects.count(),
            2,
        )

        project = Project.objects.get(
            title="Build a Django Website"
        )

        self.assertEqual(
            project.employer,
            self.employer.employer_profile,
        )

    def test_freelancer_cannot_create_project(self):
        self.authenticate(self.freelancer)

        data = {
            "title": "Unauthorized Project",
            "description": "This should fail.",
            "budget": "500.00",
            "deadline": str(
                date.today() + timedelta(days=30)
            ),
        }

        response = self.client.post(
            self.project_list_url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_authenticated_user_can_retrieve_project(self):
        self.authenticate(self.freelancer)

        response = self.client.get(
            self.project_detail_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["title"],
            "Build a REST API",
        )

    def test_project_owner_can_update_project(self):
        self.authenticate(self.employer)

        data = {
            "title": "Updated REST API",
            "description": "Updated description.",
            "budget": "2000.00",
            "deadline": str(
                date.today() + timedelta(days=60)
            ),
            "is_remote": True,
            "location": "",
        }

        response = self.client.put(
            self.project_detail_url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.project.refresh_from_db()

        self.assertEqual(
            self.project.title,
            "Updated REST API",
        )

    def test_other_employer_cannot_update_project(self):
        other_employer = User.objects.create_user(
            email="other@example.com",
            password="StrongPassword123",
            role=User.Role.EMPLOYER,
        )

        self.authenticate(other_employer)

        data = {
            "title": "Hacked Project",
            "description": "Should not be allowed.",
            "budget": "5000.00",
            "deadline": str(
                date.today() + timedelta(days=60)
            ),
            "is_remote": True,
            "location": "",
        }

        response = self.client.put(
            self.project_detail_url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_project_owner_can_delete_project(self):
        self.authenticate(self.employer)

        response = self.client.delete(
            self.project_detail_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Project.objects.filter(
                pk=self.project.pk
            ).exists()
        )