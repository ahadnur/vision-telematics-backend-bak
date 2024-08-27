from django.db import models


class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SpeedUp(TimeStamp):
    speedup = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.speedup


class CarManufacturer(TimeStamp):
    car_manufacturer = models.CharField(max_length=100)

    def __str__(self):
        return self.car_manufacturer


class PhoneManufacturer(TimeStamp):
    manufacturer = models.CharField(max_length=100)

    def __str__(self):
        return self.manufacturer


class Company(TimeStamp):
    company_name = models.CharField(max_length=100)

    def __str__(self):
        return self.company_name


class VehicleType(TimeStamp):
    vehicle_type = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def __str__(self):
        return self.vehicle_type


class VehicleMake(TimeStamp):
    vehicle_make = models.CharField(max_length=50, unique=True, null=True, blank=True)

    def __str__(self):
        return self.vehicle_make


class VehicleModel(TimeStamp):
    vehicle_model = models.CharField(max_length=50, unique=True, null=True, blank=True)
    vehicle_make = models.ForeignKey(VehicleMake, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.vehicle_model


class PhoneModel(TimeStamp):
    model_name = models.CharField(max_length=100)

    def __str__(self):
        return self.model_name


class WarrantyCallType(models.Model):
    warranty_call_type = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.warranty_call_type


class OrderType(TimeStamp):
    install_type = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.install_type
