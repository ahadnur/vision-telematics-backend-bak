from django.contrib import admin
from .models import (Customer, Invoice, InvoiceServiceLog, CustomerCompany, CustomerVehicleInfo, CustomerInstallation,
                     CustomerAddress)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['customer_ref_number', 'id']


admin.site.register(Invoice)
admin.site.register(InvoiceServiceLog)
admin.site.register(CustomerCompany)
admin.site.register(CustomerVehicleInfo)
admin.site.register(CustomerInstallation)
admin.site.register(CustomerAddress)
