from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from .serializers import SubmissionSerializer
from .permissions import IsEmployerOfContract, IsfreelancerOfContract, IsContractParticipant
from apps.contracts.models import Contract
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from apps.submissions.models import Submission
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from apps.projects.models import Project
class CreateSubmission(generics.CreateAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [
        IsAuthenticated,
        IsfreelancerOfContract
        ]

    def perform_create(self, serializer):
        contract = get_object_or_404(
            Contract,
            pk = self.kwargs['contract_id']
            )
        
        if contract.status != Contract.Status.ACTIVE:
            raise ValidationError(
                "Only active contracts accept submissions."
                )

        serializer.save(contract = contract)

class ListSubmissions(generics.ListAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [
        IsAuthenticated,
        IsEmployerOfContract
        ]
    
    def get_queryset(self):
        contract = get_object_or_404(Contract, pk = self.kwargs['contract_id'])
        self.check_object_permissions(self.request, contract)
        return contract.submissions.all()

class RetrieveSubmission(generics.RetrieveAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [
        IsAuthenticated,
        IsContractParticipant
        ]
    
    queryset = Submission.objects.all()

class ApproveSubmissionView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsEmployerOfContract,
    ]

    @transaction.atomic
    def patch(self, request, pk):

        submission = get_object_or_404(Submission, pk=pk)

        self.check_object_permissions(request, submission.contract)

        if submission.status != Submission.Status.PENDING:
            return Response(
                {"message": "This submission has already been processed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        submission.status = Submission.Status.APPROVED
        submission.save()

        contract = submission.contract
        contract.status = Contract.Status.COMPLETED
        contract.save()

        project = contract.project
        project.status = Project.Status.COMPLETED
        project.save()

        serializer = SubmissionSerializer(submission)

        return Response(
            {
                "message": "Submission approved successfully.",
                "submission": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

class RequestRevisionSubmissionView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsEmployerOfContract,
    ]

    @transaction.atomic
    def patch(self, request, pk):

        submission = get_object_or_404(Submission, pk=pk)

        self.check_object_permissions(request, submission.contract)

        if submission.status != Submission.Status.PENDING:
            return Response(
                {"message": "This submission has already been processed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        submission.status = Submission.Status.REVISION
        submission.save()

        serializer = SubmissionSerializer(submission)

        return Response(
            {
                "message": "Revision requested successfully.",
                "submission": serializer.data,
            },
            status=status.HTTP_200_OK,
        )