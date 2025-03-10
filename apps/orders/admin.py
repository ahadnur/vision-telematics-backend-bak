from django.contrib import admin
from apps.orders.models import (
    Order, 
    OrderItem, 
    Booking, 
    OrderPaymentOptions, 
    OrderOptionsData,
    OrderRefund,
    ReturnItem,
)

admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Booking)
admin.site.register(OrderPaymentOptions)
admin.site.register(OrderOptionsData)
admin.site.register(OrderRefund)
admin.site.register(ReturnItem)