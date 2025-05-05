from django.contrib import admin
from apps.orders.models import (
    Order, 
    OrderItem, 
    Booking, 
    OrderPaymentOptions, 
    OrderOptionsData,
    OrderRefund,
    ReturnItem,
    CustomerInvoice,
    EngineerInvoice,
)

admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Booking)
admin.site.register(OrderPaymentOptions)
admin.site.register(OrderOptionsData)
admin.site.register(OrderRefund)
admin.site.register(ReturnItem)


@admin.register(CustomerInvoice)
class CustomerInvoiceAdmin(admin.ModelAdmin):
    list_display = (
        'invoice_number', 'order', 'invoice_date', 'due_date',
        'total_amount', 'payment_status'
    )
    list_filter = ('invoice_date', 'due_date', 'payment_status')
    search_fields = ('invoice_number', 'order__id')
    readonly_fields = ('invoice_date', 'total_amount')
    ordering = ('-invoice_date',)


@admin.register(EngineerInvoice)
class EngineerInvoiceAdmin(admin.ModelAdmin):
    list_display = (
        'invoice_number', 'booking', 'invoice_date',
        'service_date', 'total_amount'
    )
    list_filter = ('invoice_date', 'due_date', 'service_date')
    search_fields = ('invoice_number', 'booking__id')
    ordering = ('-invoice_date',)
