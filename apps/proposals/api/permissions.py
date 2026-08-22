from rest_framework.permissions import BasePermission
from apps.accounts.models import User
from apps.projects.models import Project
from apps.proposals.models import Proposal
from django.shortcuts import get_object_or_404
class IsFreelancer(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'freelancer'

class IsProposalOwner(BasePermission):
    def has_object_permission(self, request, view, object):
        return (request.user.role == 'freelancer' and object.freelancer == request.user.freelancer_profile)

class IsProjectOwner(BasePermission):

    def has_object_permission(self, request, view, object):

        if 'project_id' not in view.kwargs.keys():
            project_id = get_object_or_404(Proposal, pk = view.kwargs['pk']).project.id
        else:
            project_id = view.kwargs['project_id']

        project = Project.objects.get(id = project_id)
        return request.user.role == User.Role.EMPLOYER and  request.user.employer_profile == project.employer