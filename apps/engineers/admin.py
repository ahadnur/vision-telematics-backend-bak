from django.contrib import admin
from apps.engineers.models import Engineer, EngineerInvoice, EngineerCompany, EngineerService, EngineerPricing

admin.site.register(Engineer)
admin.site.register(EngineerService)
admin.site.register(EngineerPricing)
admin.site.register(EngineerInvoice)
admin.site.register(EngineerCompany)
