from django.db import models


class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Bulletin(TimeStamp):
    date = models.DateField(blank=True, null=True)
    published = models.BooleanField(default=False)
    bulletin = models.TextField(blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.date} - {self.subject}"


class Credit(TimeStamp):
    name = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    original_invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE, null=True, blank=True)
    credit_note_number = models.CharField(max_length=100, blank=True, null=True)
    account = models.ForeignKey('Account', on_delete=models.SET_NULL, blank=True, null=True)
    contact_name = models.CharField(max_length=100, blank=True, null=True)
    invoice_address = models.TextField(blank=True, null=True)
    payment_method = models.CharField(max_length=100, blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    stock_supplied_to = models.CharField(max_length=100, blank=True, null=True)
    stock_returned = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    authorised = models.BooleanField(default=False)

    def __str__(self):
        return self.credit_note_number


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


class VehicleType(TimeStamp):
    vehicle_type = models.CharField(max_length=100)

    def __str__(self):
        return self.vehicle_type


class VehicleModel(TimeStamp):
    model_name = models.CharField(max_length=100)

    def __str__(self):
        return self.model_name


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


class Company(TimeStamp):
    company_name = models.CharField(max_length=100)

    def __str__(self):
        return self.company_name


class WarrantyCallType(models.Model):
    warranty_call_type = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.warranty_call_type


class OrderType(TimeStamp):
    install_type = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.install_type
