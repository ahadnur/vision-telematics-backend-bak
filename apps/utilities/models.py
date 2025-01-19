from django.db import models

from apps.common.active_manager import ActiveManager
from config.middleware import get_current_user


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)

    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveManager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        current_user = get_current_user()

        if current_user and current_user.is_authenticated:
            if not self.pk:
                self.created_by = current_user.id
            self.updated_by = current_user.id
        super(BaseModel, self).save(*args, **kwargs)


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
    type_name = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def __str__(self):
        return self.type_name


class VehicleMake(BaseModel):
    make_name = models.CharField(max_length=50, unique=True, null=True, blank=True)

    def __str__(self):
        return self.make_name


class VehicleModel(BaseModel):
    name = models.CharField(max_length=50, unique=True, null=True, blank=True)
    vehicle_make = models.ForeignKey(VehicleMake, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


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
