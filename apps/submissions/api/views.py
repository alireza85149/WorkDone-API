from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import Submission
from .permissions import IsEmployerOfProject, IsfreelancerOfContract

class CreateAndListSubmission(generics.CreateAPIView):
    serializer_class = Submission
    permission_classes = [IsAuthenticated, IsfreelancerOfContract]


# class ListSubmissions(generics.ListAPIView):


# class ApproveSubmission(generics.UpdateAPIView):


# class RequestRevisionSubmission(generics.UpdateAPIView):
