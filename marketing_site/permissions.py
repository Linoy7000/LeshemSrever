from rest_framework.permissions import BasePermission


class ProductsPermission(BasePermission):
    def has_permission(self, request, view):

        if request.method == 'POST':
            return self.has_admin_permission()

        elif request.method == 'GET':
            return True

        elif request.method == 'PUT':
            return True

        elif request.method == 'PATCH':
            return True

        elif request.method == 'DELETE':
            return self.has_admin_permission()
        return False

    def has_admin_permission(self, request):
        return request.user and request.user.is_authenticated and request.user.is_admin

