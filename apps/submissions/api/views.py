from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import SubmissionSerialzer
from .permissions import IsEmployerOfContract, IsfreelancerOfContract, IsContractParticipant
from apps.contracts.models import Contract
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

class CreateSubmission(generics.CreateAPIView):
    serializer_class = SubmissionSerialzer
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

# class ListSubmissions(generics.ListAPIView):


# class ApproveSubmission(generics.UpdateAPIView):


# class RequestRevisionSubmission(generics.UpdateAPIView):
