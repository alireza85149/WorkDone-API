from .serializers import ProposalSerializer
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.projects.models import Project
from rest_framework.permissions import IsAuthenticated
from .permissions import IsFreelancer, IsProposalOwner, IsProjectOwner
from apps.proposals.models import Proposal
from django.shortcuts import get_object_or_404
from apps.contract.models  import Contract
from django.utils import timezone
from datetime import timedelta
from django.db import transaction
class ProposalCreateView(generics.CreateAPIView):
    serializer_class = ProposalSerializer   
    permission_classes = [IsAuthenticated, IsFreelancer]
    def perform_create(self, serializer):

        project = Project.objects.get(pk = self.kwargs['project_id'])

        serializer.save(project= project, freelancer = self.request.user.freelancer_profile)

class ProposalEditView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProposalSerializer
    permission_classes = [IsAuthenticated, IsProposalOwner]

    def get_queryset(self):
        return Proposal.objects.filter(freeelancer = self.request.user.freelancer_profile)

class ProposalCheckView(generics.ListAPIView):
    serializer_class = ProposalSerializer
    permission_classes = [IsAuthenticated, IsProjectOwner]

    def get_queryset(self):
        project = get_object_or_404(Project, pk = self.kwargs['project_id'])
        return project.proposals.all()
    
class ProposalAcceptOrRejectView(APIView):
    permission_classes = [IsAuthenticated, IsProjectOwner]
    @transaction.atomic
    def patch(self, request, pk):
        proposal = get_object_or_404(Proposal, pk = pk)
        self.check_object_permissions(request, proposal)

        if proposal.status != Proposal.Status.PENDING:
            return Response(
                {"message": "Proposal has already been processed."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        elif request.data.get('status') == Proposal.Status.ACCEPTED:
            proposal.status = Proposal.Status.ACCEPTED
            proposal.save()
            Proposal.objects.filter(project = proposal.project).exclude(pk = proposal.pk).update(status = Proposal.Status.REJECTED)
            proposal.project.status = Project.Status.IN_PROGRESS
            proposal.project.save()
            contract = Contract.objects.create(
                project = proposal.project,
                proposal = proposal, 
                employer = proposal.project.employer, 
                freelancer = proposal.freelancer, 
                agreed_budget = proposal.proposed_budget,
                deadline = timezone.now() + timedelta(days=proposal.estimated_days)
                )
            return Response({'message': 'the proposal status set to Accepted.'})

        elif request.data.get('status') == Proposal.Status.REJECTED:
            proposal.status = Proposal.Status.REJECTED
            proposal.save()
            return Response({'message': 'the proposal status set to Rejected.'})

        else:
            return Response({'message': 'invlid status.'}, status = status.HTTP_400_BAD_REQUEST)


