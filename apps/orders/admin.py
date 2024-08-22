from django.contrib import admin
from apps.orders.models import Order, OrderItem

admin.site.register(OrderItem)
admin.site.register(Order)
