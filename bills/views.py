from rest_framework import viewsets

from server.globals.permissions import IsAdminPermission
from .models import Bill, Customer
from .serializers import BillSerializer, CustomerSerializer
from rest_framework.permissions import IsAuthenticated


class BillViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    permission_classes = [IsAuthenticated, IsAdminPermission]


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated, IsAdminPermission]

    def get_permissions(self):
        return super().get_permissions()
