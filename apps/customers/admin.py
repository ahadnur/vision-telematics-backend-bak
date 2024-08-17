from django.contrib import admin
from .models import Customer, Invoice, InvoiceServiceLog, CustomerCompany


admin.site.register(Customer)
admin.site.register(Invoice)
admin.site.register(InvoiceServiceLog)
admin.site.register(CustomerCompany)

