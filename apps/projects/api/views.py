from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


from apps.projects.models import Project
from .serializers import ProjectSerializer
from .permissions import IsEmployer, IsProjectOwner


class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    def get_permissions(self):

        if self.request.method == "POST":
            return [
                IsAuthenticated(),
                IsEmployer(),
            ]

        return [
            IsAuthenticated(),
        ]
    queryset = Project.objects.all()

    def perform_create(self, serializer):
        serializer.save(
            employer=self.request.user.employer_profile
        )


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    def get_permissions(self):
        if self.method == 'GET':
            return [IsAuthenticated]
        return [IsAuthenticated, IsEmployer, IsProjectOwner]
    queryset = Project.objects.all()