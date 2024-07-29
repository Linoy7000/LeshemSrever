from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BillViewSet, CustomerViewSet

router = DefaultRouter()
router.register(r'bills', BillViewSet)
router.register(r'customers', CustomerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
