from django.contrib import admin
from apps.engineers.models import Engineer, EngineerInvoice, EngineerPriority

admin.site.register(Engineer)
admin.site.register(EngineerInvoice)
admin.site.register(EngineerPriority)
