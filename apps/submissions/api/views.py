from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import SubmissionSerializer
from .permissions import IsEmployerOfContract, IsfreelancerOfContract, IsContractParticipant
from apps.contracts.models import Contract
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from apps.submissions.models import Submission

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

class ApproveSubmission(generics.UpdateAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [
        IsAuthenticated,
        IsEmployerOfContract
        ]

    def perform_update(self, serializer):

        serializer.save(
            status=Submission.Status.APPROVED
        )

class RequestRevisionSubmission(generics.UpdateAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [
        IsAuthenticated,
        IsEmployerOfContract
        ]

    def perform_update(self, serializer):

        serializer.save(
            status=Submission.Status.REVISION
        )
