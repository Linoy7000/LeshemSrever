from rest_framework import viewsets
from .models import Bill
from .serializers import BillSerializer

class BillRecordViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
