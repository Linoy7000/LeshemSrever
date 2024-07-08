import datetime

import uuid
from django.db import models
from marketing_site.models import Order
from django.core.validators import MinValueValidator, MaxValueValidator


class Customer(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)


class Bill(models.Model):
    TYPE_RECORD = [
        (1, "חיוב"),
        (2, "זיכוי"),
        (3, "תשלום")
    ]

    PAYMENT_METHOD = [
        (1, "מזומן"),
        (2, "כרטיס אשראי"),
        (3, "העברה בנקאית"),
        (4, "צ'ק")
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    record_type = models.CharField(blank=False, choices=TYPE_RECORD, default=1, max_length=50)
    quantity = models.PositiveIntegerField(blank=True, default=1)
    price = models.FloatField(blank=False)
    discount_percentage = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    comments = models.TextField(max_length=255)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orders')
    date = models.DateField(default=datetime.datetime.now())
    payment_method = models.CharField(blank=False, choices=PAYMENT_METHOD, default=1, max_length=50)
