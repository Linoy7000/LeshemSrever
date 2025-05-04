from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from logger.models import Log
from marketing_site.helpers import generate_code
from marketing_site.models import Product, Order, Contact, WebAppUser
from rest_framework import serializers
from django.contrib.auth import get_user_model
import logging

from server.globals.constants import LogLevel
from simulator.helpers import send_email

logger = logging.getLogger(__name__)
User = get_user_model()


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'email', 'first_name', 'last_name', 'is_admin')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = WebAppUser
        fields = ('first_name', 'last_name', 'password', 'email', 'is_admin')

    def create(self, validated_data):
        try:
            request = self.context.get('request')

            initial_password = generate_code()

            # Extract the password from the validated data
            password = validated_data.pop('password', initial_password)

            if password == initial_password:
                # Send code to the user email
                subject = "סיסמא עבור כניסה למערכת"
                message = f"קוד הכניסה שלך הוא {initial_password}."
                addressee = validated_data('email')
                send_email(subject, message, addressee)

            is_admin = validated_data.pop('is_admin', False)

            try:
                user = WebAppUser(**validated_data)
            except Exception as e:
                Log.objects.create(
                    level=LogLevel.ERROR,
                    payload={"message": "Failed to validate user"}
                )

            try:
                if request.user and request.user.is_admin:
                    user.is_admin = is_admin
            except Exception as e:
                pass

            user.set_password(password)  # Hashes and sets the password
            user.save()  # Save the user instance

            return user

        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Add fields to the response
        data.update({
            'is_admin': self.user.is_admin,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email,
            'phone': self.user.phone,
        })

        return data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'

    def to_internal_value(self, data):

        if 'price' in data and not data['price']:
            data['price'] = 0.0
        if 'cost' in data and not data['cost']:
            data['cost'] = 0.0

        return super(ProductSerializer, self).to_internal_value(data)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
