from django.db import models
from marketing_site.models import Order
from shared_models.models import Customer, Provider
from django.core.validators import MinValueValidator, MaxValueValidator


class Bill(models.Model):
    TYPE_RECORD = [
        (1, "חיוב"),
        (2, "זיכוי"),
        (3, "תשלום")
    ]

    PAYMENT_METHOD = [
        (1, "מזומן"),
        (2, "כרטיס אשראי"),
        (3, "העברה בנקאית")
    ]
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE),
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE),
    type=models.CharField(blank=False, choices=TYPE_RECORD, max_length=50),
    quantity=models.PositiveIntegerField(default=1),
    price=models.FloatField(default=0.0),
    discount_percentage = models.DecimalField(
        default=0.0,
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    ),
    description = models.TextField(),
    order=models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orders'),
    date=models.DateField(),
    invoice_num = models.CharField(max_length=50),
    payment_method=models.CharField(blank=False, choices=PAYMENT_METHOD, max_length=50),
