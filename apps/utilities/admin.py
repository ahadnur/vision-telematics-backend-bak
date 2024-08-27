from django.contrib import admin
from .models import (PhoneModel, VehicleModel, VehicleMake, VehicleType, OrderType, PhoneManufacturer, CarManufacturer,
                     WarrantyCallType, SpeedUp, Company)


admin.site.register(PhoneModel)
admin.site.register(VehicleModel)
admin.site.register(VehicleType)
admin.site.register(VehicleMake)
admin.site.register(OrderType)
admin.site.register(PhoneManufacturer)
admin.site.register(CarManufacturer)
admin.site.register(WarrantyCallType)
admin.site.register(SpeedUp)
admin.site.register(Company)
