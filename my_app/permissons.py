from rest_framework.permissions import BasePermission


class Cheak(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        elif request.method == 'POST':
            return request.user
        elif request.method == 'DELETE':
            return request.user.is_superuser
        else:
            return request.user == view.get_object().user_id
