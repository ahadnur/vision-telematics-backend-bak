from django.contrib import admin
from apps.services.models import Service, CustomerCare

admin.site.register(CustomerCare)
admin.site.register(Service)
