from rest_framework.permissions import BasePermission

from repo.models import Repo, Class


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Repo):
            return obj.owner == request.user
        return False
