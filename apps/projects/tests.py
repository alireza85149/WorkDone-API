from datetime import date

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import User, EmployerProfile, FreelancerProfile
from apps.projects.models import Project


class ProjectTests(APITestCase):

    def setUp(self):
        # Employer
        self.employer = User.objects.create_user(
            email="employer@example.com",
            password="StrongPassword123",
            role=User.Role.EMPLOYER,
        )

        self.employer_profile = EmployerProfile.objects.create(
            user=self.employer,
            company_name="Test Company",
        )

        # Freelancer
        self.freelancer = User.objects.create_user(
            email="freelancer@example.com",
            password="StrongPassword123",
            role=User.Role.FREELANCER,
        )

        self.freelancer_profile = FreelancerProfile.objects.create(
            user=self.freelancer,
            first_name="John",
            last_name="Doe",
        )

        self.list_url = reverse("project-list-create")

    def authenticate(self, user):
        response = self.client.post(
            reverse("login"),
            {
                "email": user.email,
                "password": "StrongPassword123",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {response.data['access']}"
        )

    def project_data(self):
        return {
            "title": "Build a Django API",
            "description": "Build a REST API for a freelancing platform.",
            "budget": "1500.00",
            "deadline": "2026-12-31",
            "location": "Remote",
            "is_remote": True,
        }

    def test_employer_can_create_project(self):
        self.authenticate(self.employer)

        response = self.client.post(
            self.list_url,
            self.project_data(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            Project.objects.count(),
            1,
        )

        project = Project.objects.first()

        self.assertEqual(
            project.employer,
            self.employer_profile,
        )

        self.assertEqual(
            project.title,
            "Build a Django API",
        )

    def test_freelancer_cannot_create_project(self):
        self.authenticate(self.freelancer)

        response = self.client.post(
            self.list_url,
            self.project_data(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_unauthenticated_user_cannot_create_project(self):
        response = self.client.post(
            self.list_url,
            self.project_data(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_authenticated_user_can_list_projects(self):
        Project.objects.create(
            employer=self.employer_profile,
            title="Existing Project",
            description="Test description",
            budget="1000.00",
            deadline=date(2026, 12, 31),
        )

        self.authenticate(self.freelancer)

        response = self.client.get(
            self.list_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

    def test_project_owner_can_retrieve_project(self):
        project = Project.objects.create(
            employer=self.employer_profile,
            title="My Project",
            description="Test description",
            budget="1000.00",
            deadline=date(2026, 12, 31),
        )

        self.authenticate(self.employer)

        url = reverse(
            "project-detail",
            kwargs={"pk": project.pk},
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["title"],
            "My Project",
        )

    def test_freelancer_can_retrieve_project(self):
        project = Project.objects.create(
            employer=self.employer_profile,
            title="Public Project",
            description="Test description",
            budget="1000.00",
            deadline=date(2026, 12, 31),
        )

        self.authenticate(self.freelancer)

        url = reverse(
            "project-detail",
            kwargs={"pk": project.pk},
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_other_employer_cannot_update_project(self):
        other_employer = User.objects.create_user(
            email="other@example.com",
            password="StrongPassword123",
            role=User.Role.EMPLOYER,
        )

        EmployerProfile.objects.create(
            user=other_employer,
            company_name="Other Company",
        )

        project = Project.objects.create(
            employer=self.employer_profile,
            title="Original Project",
            description="Original description",
            budget="1000.00",
            deadline=date(2026, 12, 31),
        )

        self.authenticate(other_employer)

        url = reverse(
            "project-detail",
            kwargs={"pk": project.pk},
        )

        response = self.client.patch(
            url,
            {
                "title": "Hacked Project",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_project_owner_can_update_project(self):
        project = Project.objects.create(
            employer=self.employer_profile,
            title="Original Project",
            description="Original description",
            budget="1000.00",
            deadline=date(2026, 12, 31),
        )

        self.authenticate(self.employer)

        url = reverse(
            "project-detail",
            kwargs={"pk": project.pk},
        )

        response = self.client.patch(
            url,
            {
                "title": "Updated Project",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        project.refresh_from_db()

        self.assertEqual(
            project.title,
            "Updated Project",
        )

    def test_project_owner_can_delete_project(self):
        project = Project.objects.create(
            employer=self.employer_profile,
            title="Delete Me",
            description="Test description",
            budget="1000.00",
            deadline=date(2026, 12, 31),
        )

        self.authenticate(self.employer)

        url = reverse(
            "project-detail",
            kwargs={"pk": project.pk},
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Project.objects.filter(pk=project.pk).exists()
        )