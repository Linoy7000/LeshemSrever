from django.contrib import admin

from marketing_site.models import Product, Order, OrderItem, Contact

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Contact)