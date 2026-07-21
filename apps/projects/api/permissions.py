from rest_framework.permissions import BasePermission


class IsEmployer(BasePermission):

    def has_permission(self, request, view):
        return request.user.role == "employer"
        
class IsProjectOwner(BasePermission):

    def has_object_permission(self, request, view, object):
        return request.user.emplyer_profile == object.employer