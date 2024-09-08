from django.contrib import admin
from apps.orders.models import Order, OrderItem, Booking

admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Booking)
