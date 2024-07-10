from rest_framework.permissions import BasePermission


class UserOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['DELETE','PATCH']:
            return obj.username == request.user.username
        return True
    