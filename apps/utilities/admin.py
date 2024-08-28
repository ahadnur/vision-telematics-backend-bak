from django.contrib import admin
from .models import (PhoneModel, VehicleModel, VehicleMake, VehicleType, OrderType, PhoneManufacturer, CarManufacturer,
                     WarrantyCallType, SpeedUp, Company)


@admin.register(VehicleMake)
class VehicleMakeAdmin(admin.ModelAdmin):
    list_display = ['vehicle_make', 'id']


@admin.register(VehicleType)
class VehicleTypeAdmin(admin.ModelAdmin):
    list_display = ['vehicle_type', 'id']


@admin.register(VehicleModel)
class VehicleModelAdmin(admin.ModelAdmin):
    list_display = ['vehicle_model', 'id']


admin.site.register(OrderType)
admin.site.register(PhoneManufacturer)
admin.site.register(CarManufacturer)
admin.site.register(WarrantyCallType)
admin.site.register(SpeedUp)
admin.site.register(Company)
