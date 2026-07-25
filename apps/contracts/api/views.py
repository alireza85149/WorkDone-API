from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsContractParticipant, IsEmpoloyerOfContract
from apps.contracts.models import Contract
from apps.projects.models import Project
from django.shortcuts import get_object_or_404
from .serializers import ContractSerializer
from django.db import transaction

class CompleteContractView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsEmployerOfContract,
    ]

    @transaction.Atomic
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

    @transaction.Atomic
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

