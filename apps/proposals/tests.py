from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import (
    User, 
    EmployerProfile,
    FreelancerProfile,
)

from apps.projects.models import Project
from apps.proposals.models import Proposal

class ProposalTests(APITestCase):

    def setUp(self):

        self.employer = User.objects.create_user(
            email="employer@example.com",
            password="StrongPassword123",
            role=User.Role.EMPLOYER,
        )

        self.employer_profile = EmployerProfile.objects.create(
            user=self.employer,
            company_name="Test Company",
        )

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

        self.project = Project.objects.create(
            employer=self.employer_profile,
            title="Test Project",
            description="A project for testing proposals.",
            budget=1000,
            deadline="2026-12-31",
        )
        
        self.create_url = reverse(
            'proposal-create',
            kwargs={'project_id':self.project.id}
        )

        self.check_url = reverse(
            'proposal-check',
            kwargs={'project_id':self.project.id}
        )

    def test_freelancer_can_create_proposal(self):

        self.client.force_authenticate(
            user=self.freelancer
        )

        data = {
            "cover_letter": "I am interested in this project.",
            "proposed_budget": 1200,
            "estimated_days": 20,
        }

        response = self.client.post(
            self.create_url,
            data,
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        proposal = Proposal.objects.get(
            project=self.project,
            freelancer=self.freelancer_profile,
        )

        self.assertEqual(
            proposal.cover_letter,
            "I am interested in this project."
        )

        self.assertEqual(
            proposal.proposed_budget,
            1200
        )

        self.assertEqual(
            proposal.estimated_days,
            20
        )

        self.assertEqual(
            proposal.status,
            Proposal.Status.PENDING
        )

    def test_employer_cannot_create_proposal(self):

        self.client.force_authenticate(
            user=self.employer
        )

        data = {
            "cover_letter": "I want to apply.",
            "proposed_budget": 1000,
            "estimated_days": 10,
        }

        response = self.client.post(
            self.create_url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.assertEqual(
            Proposal.objects.count(),
            0,
        )

    def test_unauthenticated_user_cannot_create_proposal(self):

        data = {
            "cover_letter": "I want to apply.",
            "proposed_budget": 1000,
            "estimated_days": 10,
        }

        response = self.client.post(
            self.create_url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

        self.assertEqual(
            Proposal.objects.count(),
            0,
        )

    def test_freelancer_cannot_create_duplicate_proposal(self):

        Proposal.objects.create(
            project=self.project,
            freelancer=self.freelancer_profile,
            cover_letter="First proposal",
            proposed_budget=1000,
            estimated_days=15,
        )

        self.client.force_authenticate(
            user=self.freelancer
        )

        data = {
            "cover_letter": "Second proposal",
            "proposed_budget": 1200,
            "estimated_days": 20,
        }

        response = self.client.post(
            self.create_url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_freelancer_can_check_proposal(self):

        proposal = Proposal.objects.create(
            project=self.project,
            freelancer=self.freelancer_profile,
            cover_letter="I am interested.",
            proposed_budget=1200,
            estimated_days=20,
        )

        self.client.force_authenticate(
            user=self.freelancer
        )

        response = self.client.get(
            self.check_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data[0]["id"],
            proposal.id,
        )

    def test_unauthenticated_user_cannot_check_proposal(self):

        response = self.client.get(
            self.check_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def create_proposal(self):

        return Proposal.objects.create(
            project=self.project,
            freelancer=self.freelancer_profile,
            cover_letter="I am interested.",
            proposed_budget=1200,
            estimated_days=20,
        )

    def test_project_owner_can_accept_proposal(self):

        proposal = self.create_proposal()

        self.client.force_authenticate(
            user=self.employer
        )

        url = reverse(
            "proposal-accept-or-deny",
            kwargs={"pk": proposal.id},
        )

        response = self.client.patch(
            url,
            {"status": Proposal.Status.ACCEPTED},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        proposal.refresh_from_db()

        self.assertEqual(
            proposal.status,
            Proposal.Status.ACCEPTED,
        )

    def test_project_owner_can_reject_proposal(self):

        proposal = self.create_proposal()

        self.client.force_authenticate(
            user=self.employer
        )

        url = reverse(
            "proposal-accept-or-deny",
            kwargs={"pk": proposal.id},
        )

        response = self.client.patch(
            url,
            {"status": Proposal.Status.REJECTED},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        proposal.refresh_from_db()

        self.assertEqual(
            proposal.status,
            Proposal.Status.REJECTED,
        )

    def test_other_employer_cannot_accept_or_reject_proposal(self):

        proposal = self.create_proposal()

        other_employer = User.objects.create_user(
            email="other@example.com",
            password="StrongPassword123",
            role=User.Role.EMPLOYER,
        )

        EmployerProfile.objects.create(
            user=other_employer,
            company_name="Other Company",
        )

        self.client.force_authenticate(
            user=other_employer
        )

        url = reverse(
            "proposal-accept-or-deny",
            kwargs={"pk": proposal.id},
        )

        response = self.client.patch(
            url,
            {"status": Proposal.Status.ACCEPTED},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_freelancer_cannot_accept_or_reject_proposal(self):

        proposal = self.create_proposal()

        self.client.force_authenticate(
            user=self.freelancer
        )

        url = reverse(
            "proposal-accept-or-deny",
            kwargs={"pk": proposal.id},
        )

        response = self.client.patch(
            url,
            {"status": Proposal.Status.ACCEPTED},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )