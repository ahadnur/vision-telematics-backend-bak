from django.contrib import admin
from apps.orders.models import Order, KIF
# Register your models here.

admin.site.register(KIF)
admin.site.register(Order)
