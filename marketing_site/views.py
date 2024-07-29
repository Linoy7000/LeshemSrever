
from datetime import timedelta

from django.utils import timezone
from rest_framework import viewsets
from rest_framework.views import APIView
from marketing_site.models import Product, Order, Contact, WebAppUser
from marketing_site.serializers import ProductSerializer, OrderSerializer, ContactSerializer

from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .helpers import generate_otp_code, send_email
from .permissions import ProductsPermission
from .serializers import RegisterSerializer, ChangePasswordSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = WebAppUser.objects.all()
    serializer_class = RegisterSerializer


#TODO
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({"status": "success"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ObtainOTPTokenView(APIView):

    def post(self, request, *args, **kwargs):

        password = request.data.get('password')
        email = request.data.get('email')

        # Get the current user
        user = WebAppUser.objects.filter(email=email).first()

        # Check password validation and generate OTP code if Admin
        if user and user.check_password(password) and user.is_admin:
            # Generate random code
            otp_code = generate_otp_code()
            # Save code for the current user
            user.otp_code = otp_code
            # Set expire time to 10 minutes
            user.otp_expires_at = timezone.now() + timedelta(minutes=10)
            user.save()
            # Send code to the user email
            subject = "קוד אימות עבור כניסה למערכת"
            message = f"קוד הכניסה שלך הוא {otp_code}. \n הקוד תקף ל-10 דקות."
            addressee = user.email
            send_email(subject, message, addressee)

            return Response({'message': 'קוד חד פעמי נשלח לכתובת המייל המעודכנת במערכת'}, status=status.HTTP_200_OK)

        return Response({'message': 'משתמש לא נמצא'}, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPTokenView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        otp_code = request.data.get('otp_code')

        # Get the current user
        user = WebAppUser.objects.filter(email=email).first()
        # Check OTP code validation
        if user and user.otp_code == otp_code and user.otp_expires_at > timezone.now():
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        return Response({'message': 'הקוד שהוזן שגוי או לא תקף'}, status=status.HTTP_400_BAD_REQUEST)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'uuid'
    permission_classes = [ProductsPermission]

    def get_queryset(self):
        queryset = Product.objects.all()
        category = self.request.query_params.get('category', None)
        price = self.request.query_params.get('price', None)
        if category is not None:
            queryset = queryset.filter(category=category)
        if price is not None:
            queryset = queryset.filter(price=price)
        return queryset


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        queryset = Order.objects.all()
        customer = self.request.query_params.get('customer', None)
        if customer is not None:
            queryset = queryset.filter(customer=customer)
        return queryset


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    lookup_field = 'uuid'
