from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BillRecordViewSet

router = DefaultRouter()
router.register(r'bills/', BillRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
