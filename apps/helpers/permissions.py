from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import BasePermission


class IsUser(BasePermission):
    message = 'User is not authenticated'

    def has_permission(self, request, view):
        # if user is not authenticated, return False
        if request.user is None or isinstance(request.user, AnonymousUser):
            return False

        # if request was made using client credentials, return False
        if request.user.username == 'bmu_user':
            return False
        return True
