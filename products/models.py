from django.db import models


class Category(models.Model):
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
    sant = models.BooleanField(default=False)
    alead = models.BooleanField(default=False)
    ndbkt = models.BooleanField(default=False)
    lcon = models.BooleanField(default=False)
    bluetooth_ff = models.BooleanField(default=False)
    pkg1 = models.BooleanField(default=False)
    pkg2 = models.BooleanField(default=False)
    pkg3 = models.BooleanField(default=False)
    pkg4 = models.BooleanField(default=False)
    pkg5 = models.BooleanField(default=False)
    pkg6 = models.BooleanField(default=False)
    pkg7 = models.BooleanField(default=False)
    pkg8 = models.BooleanField(default=False)
    pkg9 = models.BooleanField(default=False)
    pkg0 = models.BooleanField(default=False)

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
    bracket = models.BooleanField(default=False)
    brodit = models.BooleanField(default=False)
    mounting_notes = models.TextField(blank=True, null=True)
    mute_pin = models.CharField(max_length=100, blank=True, null=True)
    vehicle_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.marque} - {self.range}"


class KIF(models.Model):
    order = models.ForeignKey('Order', on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    qty = models.PositiveIntegerField()
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    credit_note = models.CharField(max_length=100, null=True, blank=True)
    returned = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Order {self.order.id} - Product {self.product.id}"

    class Meta:
        verbose_name_plural = "KIFs"



