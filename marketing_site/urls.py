from rest_framework.routers import DefaultRouter
from marketing_site.views import ProductViewSet, OrderViewSet, ContactViewSet, ObtainOTPTokenView, VerifyOTPTokenView
from django.urls import include

from django.urls import path
from .views import RegisterView, ChangePasswordView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'contacts', ContactViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin-login/', ObtainOTPTokenView.as_view(), name='obtain_otp_token'),
    path('verify-otp/', VerifyOTPTokenView.as_view(), name='verify_otp_token'),
]
