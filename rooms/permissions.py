from rest_framework import permissions

class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 2


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 3