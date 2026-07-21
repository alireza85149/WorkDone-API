from .serializers import ProposalSerializer
from rest_framework import generics
from projects.models import Project
from rest_framework.permissions import IsAuthenticated
from .permissions import IsFreelancer
class PropsalCreateView(generics.CreateAPIView):
    serializer_class = ProposalSerializer   
    permission_classes = [IsAuthenticated, IsFreelancer]
    def perform_create(self, serializer):

        project = Project.objects.get(pk = self.kwargs['project_id'])

        serializer.save(project= project, freelancer = self.request.user.freelancer_profile)

