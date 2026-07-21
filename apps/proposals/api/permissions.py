from rest_framework.permissions import BasePermission

class IsFreelancer(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'freelancer'
