from rest_framework.routers import DefaultRouter
from marketing_site.views import ProductViewSet, OrderViewSet, ContactViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'products/', ProductViewSet)
router.register(r'orders/', OrderViewSet)
router.register(r'contacts/', ContactViewSet)

urlpatterns = [
    path('', include(router.urls)),
]