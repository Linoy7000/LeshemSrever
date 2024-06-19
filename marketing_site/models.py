import uuid
from django.db import models

from shared_models.models import Customer


class Product(models.Model):
    CATEGORY_CHOICES = [
        (1, 'פרוכות'),
        (2, 'ספרי תורה'),
        (3, 'בימה'),
        (4, 'שונות')
    ]
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    category = models.PositiveIntegerField(blank=False, choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=255, blank=False)
    link = models.CharField(blank=False, max_length=150)
    price = models.FloatField(blank=True, null=True)
    cost = models.FloatField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    sales = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)


class Order(models.Model):
    STATUS_CHOICES = [
        (1, "טיוטא"),
        (2, "סגורה"),
        (3, "שולמה")
    ]
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    discount_percentage = models.FloatField(blank=True, default=0.00)
    discount = models.FloatField(blank=True, default=0.00)
    status = models.PositiveIntegerField(blank=False, default=1, choices=STATUS_CHOICES)
    supply = models.DateField(blank=True, null=True)
    close_date = models.DateTimeField(blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)


class OrderItem(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class Contact(models.Model):
    SUBJECT_CHOICES = [
        (1, 'פרוכות'),
        (2, 'ספרי תורה'),
        (3, 'בימה'),
        (4, 'אחר')
    ]
    STATUS_CHICES = [
        (1, 'פתוחה'),
        (2, 'סגורה')
    ]
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    subject = models.PositiveIntegerField(choices=SUBJECT_CHOICES)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.PositiveIntegerField(choices=STATUS_CHICES, default=1)

    def __str__(self):
        return f'{self.name} - {self.subject}'
