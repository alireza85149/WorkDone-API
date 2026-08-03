from rest_framework.permissions import BasePermission
from apps.accounts.models import User
class IsEmployerOfContract(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.role == User.Role.EMPLOYER 
            and 
            request.user.Employer_profile == obj.contract.employer
        )

class IsfreelancerOfContract(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.role == User.Role.FREELANCER 
            and 
            request.user.Freelancer_profile == obj.contract.freelancer
        )

class IsContractParticipant(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.role == User.Role.FREELANCER 
            and 
            request.user.Freelancer_profile == obj.contract.freelancer
        ) or (
            request.user.role == User.Role.EMPLOYER 
            and 
            request.user.Employer_profile == obj.contract.employer
        )