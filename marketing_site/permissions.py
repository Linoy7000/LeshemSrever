from rest_framework.permissions import BasePermission, AllowAny


class ProductsPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return [AllowAny()]

        return self.has_admin_permission(request)

    @staticmethod
    def has_admin_permission(request):
        return request.user and request.user.is_authenticated and request.user.is_admin
