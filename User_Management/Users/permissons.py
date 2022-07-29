from rest_framework import permissions


class UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        """
            This function is used for when user is login then don`t show the POST Operation For user
        """
        if request.method == 'POST' and request.user.is_authenticated:
            return False
        else:
            return True
