from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True


class SpeedUp(BaseModel):
    speedup = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.speedup


class CarManufacturer(BaseModel):
    car_manufacturer = models.CharField(max_length=100)

    def __str__(self):
        return self.car_manufacturer


class PhoneManufacturer(BaseModel):
    manufacturer = models.CharField(max_length=100)

    def __str__(self):
        return self.manufacturer


class Company(BaseModel):
    company_name = models.CharField(max_length=100)

    def __str__(self):
        return self.company_name


class VehicleType(BaseModel):
    vehicle_type = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def __str__(self):
        return self.vehicle_type


class VehicleMake(BaseModel):
    vehicle_make = models.CharField(max_length=50, unique=True, null=True, blank=True)

    def __str__(self):
        return self.vehicle_make


class VehicleModel(BaseModel):
    vehicle_model = models.CharField(max_length=50, unique=True, null=True, blank=True)
    vehicle_make = models.ForeignKey(VehicleMake, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.vehicle_model


class PhoneModel(BaseModel):
    model_name = models.CharField(max_length=100)

    def __str__(self):
        return self.model_name


class WarrantyCallType(models.Model):
    warranty_call_type = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.warranty_call_type


class OrderType(BaseModel):
    install_type = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.install_type
