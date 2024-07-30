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
    vehicle_type = models.CharField(max_length=100)

    def __str__(self):
        return self.vehicle_type


class VehicleModel(TimeStamp):
    model_name = models.CharField(max_length=100)

    def __str__(self):
        return self.model_name


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




