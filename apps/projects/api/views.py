from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


from apps.projects.models import Project
from .serializers import ProjectSerializer


class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.all()

    def perform_create(self, serializer):
        serializer.save(
            employer=self.request.user.employer_profile
        )


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    queryset = Project.objects.all()