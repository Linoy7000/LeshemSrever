from django.shortcuts import render
from rest_framework import viewsets

from marketing_site.models import Product, Order, Contact
from marketing_site.serializers import ProductSerializer, OrderSerializer, ContactSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

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

    def get_queryset(self):
        queryset = Order.objects.all()
        customer = self.request.query_params.get('customer', None)
        if customer is not None:
            queryset = queryset.filter(customer=customer)
        return queryset


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer