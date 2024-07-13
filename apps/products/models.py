from django.db import models
from apps.utilities.models import TimeStamp


class Category(TimeStamp):
    category_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_name = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    pkg0 = models.CharField(max_length=255, null=True, blank=True)
    pkg1 = models.CharField(max_length=255, null=True, blank=True)
    pkg2 = models.CharField(max_length=255, null=True, blank=True)
    pkg3 = models.CharField(max_length=255, null=True, blank=True)
    pkg4 = models.CharField(max_length=255, null=True, blank=True)
    pkg5 = models.CharField(max_length=255, null=True, blank=True)
    pkg6 = models.CharField(max_length=255, null=True, blank=True)
    pkg7 = models.CharField(max_length=255, null=True, blank=True)
    pkg8 = models.CharField(max_length=255, null=True, blank=True)
    pkg9 = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.product_name


class CarData(models.Model):
    marque = models.CharField(max_length=100, blank=True, null=True)
    range = models.CharField(max_length=100, blank=True, null=True)
    from_year = models.IntegerField(blank=True, null=True)
    to_year = models.IntegerField(blank=True, null=True)
    spec_notes = models.TextField(blank=True, null=True)
    telemute = models.BooleanField(default=False)
    kram = models.BooleanField(default=False)
    mounting_notes = models.TextField(blank=True, null=True)
    mute_pin = models.CharField(max_length=100, blank=True, null=True)
    vehicle_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.marque} - {self.range}"




