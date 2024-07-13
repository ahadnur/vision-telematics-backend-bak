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


class PasteError(TimeStamp):
    sku = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    qty = models.IntegerField(blank=True, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.sku


class CarManufacturer(TimeStamp):
    car_manufacturer = models.CharField(max_length=100)

    def __str__(self):
        return self.car_manufacturer


class PhoneManufacturer(TimeStamp):
    manufacturer = models.CharField(max_length=100)

    def __str__(self):
        return self.manufacturer


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



