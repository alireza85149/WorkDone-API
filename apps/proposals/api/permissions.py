from rest_framework.permissions import BasePermission
from projects.models import Project
class IsFreelancer(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'freelancer'

class IsProposalOwner(BasePermission):
    def has_object_permission(self, request, view, object):
        return (request.user.role == 'freelancer' and object.freelancer == request.user.freelancer_profile)

class IsProjectOwner(BasePermission):

    def has_object_permission(self, request, view, object):
        project = Project.objects.get(id = request.kwargs['project_id'])
        return request.user.emplyer_profile == project.employer