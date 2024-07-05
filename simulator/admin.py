from django.contrib import admin

from marketing_site.models import Product, Order, OrderItem, Contact
from shared_models.models import Customer
from simulator.models import Type, Element, TrainingData

# Simulator
admin.site.register(Type)
admin.site.register(Element)
admin.site.register(TrainingData)
