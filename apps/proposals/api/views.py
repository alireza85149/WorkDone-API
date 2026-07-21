from .serializers import ProposalSerializer
from rest_framework import generics
from projects.models import Project

class PropsalCreateView(generics.CreateAPIView):
    serializer_class = ProposalSerializer

    def perform_create(self, serializer):

        project = Project.objects.get(pk = self.kwargs['project_id'])

        serializer.save(project= project, freelancer = self.request.user.freelancer_profile)
