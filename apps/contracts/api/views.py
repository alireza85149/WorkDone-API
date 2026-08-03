from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsContractParticipant, IsEmployerOfContract
from apps.contracts.models import Contract
from apps.projects.models import Project
from apps.accounts.models import User
from django.shortcuts import get_object_or_404
from .serializers import ContractSerializer
from django.db import transaction

class CompleteContractView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsEmployerOfContract,
    ]

    @transaction.atomic
    def patch(self, request, pk):
        contract = get_object_or_404(Contract, pk = pk)
        self.check_object_permissions(request, contract)
        if contract.status != Contract.Status.ACTIVE:
            return Response({'message': 'the contract is not changeable'}, status = status.HTTP_400_BAD_REQUEST)
        contract.status = Contract.Status.COMPLETED
        contract.save()

        contract.project.status = Project.Status.CANCELLED
        contract.project.save()

        serializer = ContractSerializer(contract)
        return Response({'message': 'the contract completed', 'contract':serializer.data})

class CancelContractView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsContractParticipant
    ]

    @transaction.atomic
    def patch(self, request, pk):
        contract = get_object_or_404(Contract, pk = pk)
        self.check_object_permissions(request, contract)
        if contract.status != Contract.Status.ACTIVE:
            return Response({'message': 'the contract is not changeable'},
                             status = status.HTTP_400_BAD_REQUEST)
        contract.status = Contract.Status.CANCELLED
        contract.save()

        contract.project.status = Project.Status.COMPLETED
        contract.project.save()

        serializer = ContractSerializer(contract)
        return Response({'message': 'the contract canceled', 'contract':serializer.data})

class RetrieveContractView(generics.RetrieveAPIView):

    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated, IsContractParticipant]

    queryset = Contract.objects.all()


class ListContractView(generics.ListAPIView):

    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == User.Role.EMPLOYER:
            return Contract.objects.filter(employer = self.request.user.employer_profile)
        elif self.request.user.role == User.Role.FREELANCER:
            return Contract.objects.filter(freelancer = self.request.user.freelancer_profile)
        return Contract.objects.none()
