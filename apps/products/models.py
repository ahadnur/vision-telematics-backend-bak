from django.db import models
from apps.utilities.models import TimeStamp


class Supplier(TimeStamp):
    supplier_name = models.CharField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.supplier_name


"""
When the company needs to purchase products or services from suppliers
to fulfill customer orders or maintain inventory, they generate purchase orders.
These purchase orders are recorded in the PO table, which helps track the items
to be procured, their quantities, descriptions, and associated suppliers
"""


class PO(TimeStamp):
    po_ref = models.CharField(max_length=100, unique=True)
    invoice_number = models.ForeignKey('customers.Invoice', on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()
    description = models.TextField(null=True, blank=True)
    supplier = models.ForeignKey('Supplier', on_delete=models.SET_NULL, null=True, blank=True)
    item_po = models.CharField(max_length=100, null=True, blank=True)
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, blank=True)
    supplier_po = models.CharField(max_length=100, null=True, blank=True)
    item_ordered = models.CharField(max_length=255, null=True, blank=True)
    received = models.BooleanField(default=False)
    qty = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.po_ref


class StockControlCode(models.Model):
    code = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.code


class StockSuppliedTo(models.Model):
    stock_supplied_to = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.stock_supplied_to


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
    stock_code = models.ForeignKey(StockControlCode, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
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


# ProductSKU
class PasteError(TimeStamp):
    # sku means `Stock Keeping Unit`
    sku = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    qty = models.IntegerField(blank=True, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.sku


