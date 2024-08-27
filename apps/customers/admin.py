from django.contrib import admin
from .models import (Customer, Invoice, InvoiceServiceLog, CustomerCompany, CustomerVehicleInfo, CustomerInstallation,
                     CustomerAddress)


admin.site.register(Customer)
admin.site.register(Invoice)
admin.site.register(InvoiceServiceLog)
admin.site.register(CustomerCompany)
admin.site.register(CustomerVehicleInfo)
admin.site.register(CustomerInstallation)
admin.site.register(CustomerAddress)
