from django.contrib import admin
from .models import (Customer, Invoice, InvoiceServiceLog, CustomerVehicle, CustomerInstallation,
                     CustomerAddress, CustomerFeedback)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['customer_ref_number', 'contact_name', 'id']


admin.site.register(Invoice)
admin.site.register(InvoiceServiceLog)
admin.site.register(CustomerVehicle)
admin.site.register(CustomerInstallation)
admin.site.register(CustomerAddress)

@admin.register(CustomerFeedback)
class CustomerFeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'product', 'rating', 'status', 'created_at')
    list_display_links = ('id', 'customer', 'product')
    list_filter = ('status', 'rating', 'created_at', 'product')
    search_fields = ('customer__name', 'product__name', 'feedback')
    readonly_fields = ('created_at',)
    ordering = ['-created_at']