from rest_framework.permissions import BasePermission
from apps.accounts.models import User
class IsContractParticipant(BasePermission):
        
    def has_object_permission(self, request, view, object):
        return (
            object.freelancer == request.user.freelancer_profile
            or
            object.employer == request.user.employer_profile
        )

class IsEmployerOfContract(BasePermission):

    def has_object_permission(self, request, view, object):
        return (request.user.role == User.Role.EMPLOYER and request.user.employer_profile == object.employer)