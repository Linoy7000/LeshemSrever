import uuid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

from bills.models import Customer, Bill
from server.constants import ProductCategories, OrderStatus, ContactSubject, ContactStatus

    


class Product(models.Model):
    CATEGORY_CHOICES = [
        (ProductCategories.PAROCHET, 'פרוכות'),
        (ProductCategories.SEFER_TORA, 'ספרי תורה'),
        (ProductCategories.BIMA, 'בימה'),
        (ProductCategories.OTHER, 'שונות')
    ]
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    category = models.PositiveIntegerField(blank=False, choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=255, blank=False)
    url = models.CharField(blank=False, max_length=150)
    local_link = models.CharField(blank=False, max_length=255, default=1)
    price = models.FloatField(blank=True, null=True)
    cost = models.FloatField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    sales = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"ID: {self.id} | {self.get_category_display()} - {self.url}"


class Order(models.Model):
    STATUS_CHOICES = [
        (OrderStatus.DRAFT, "טיוטא"),
        (OrderStatus.CLOSED, "סגורה"),
        (OrderStatus.PAID, "שולמה")
    ]
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    discount_percentage = models.FloatField(blank=True, null=True, default=0.00)
    discount = models.FloatField(blank=True, null=True, default=0.00)
    status = models.PositiveIntegerField(blank=False, default=1, choices=STATUS_CHOICES)
    supply = models.DateField(blank=True, null=True)
    close_date = models.DateTimeField(blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
    bill = models.ForeignKey(Bill, on_delete=models.PROTECT)


class OrderItem(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.order} - {self.id}"


class Contact(models.Model):
    SUBJECT_CHOICES = [
        (ContactSubject.PAROCHET, 'פרוכות'),
        (ContactSubject.SEFER_TORA, 'ספרי תורה'),
        (ContactSubject.BIMA, 'בימה'),
        (ContactSubject.OTHER, 'אחר')
    ]
    STATUS_CHICES = [
        (ContactStatus.OPEN, 'פתוחה'),
        (ContactStatus.CLOSED, 'סגורה')
    ]
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    subject = models.CharField(max_length=10, choices=SUBJECT_CHOICES)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.PositiveIntegerField(choices=STATUS_CHICES, default=1)

    def __str__(self):
        return f'{self.name} - {self.subject}'

class WebAppUserManager(BaseUserManager):

    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """ Create superuser (for django admin) """
        user = self.model(email=email, is_active=True, is_superuser=True, is_staff=True, is_admin=True, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user



class WebAppUser(AbstractBaseUser, PermissionsMixin):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    first_name = models.CharField(max_length=255, blank=False)
    last_name = models.CharField(max_length=255, blank=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    otp_code = models.CharField(max_length=255, blank=True, null=True)
    otp_expires_at = models.DateTimeField(blank=True, null=True)

    objects = WebAppUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password']

    def __str__(self):
        return self.email

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
