from django.db import models
from apps.utilities.models import BaseModel
from .product_model import Product


class Supplier(BaseModel):
    supplier_name = models.CharField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'products_supplier'
        ordering = ['-created_at']

    def __str__(self):
        return self.supplier_name


"""
When the company needs to purchase products or services from suppliers
to fulfill customer orders or maintain inventory, they generate purchase orders.
These purchase orders are recorded in the PO table, which helps track the items
to be procured, their quantities, descriptions, and associated suppliers
"""


class PO(BaseModel):
    po_ref = models.CharField(max_length=100, unique=True)
    invoice_number = models.CharField(max_length=255, null=True, blank=True, unique=True)
    date = models.DateField()
    description = models.TextField(null=True, blank=True)
    supplier = models.ForeignKey('Supplier', on_delete=models.SET_NULL, null=True, blank=True)
    item_po = models.CharField(max_length=100, null=True, blank=True)
    product_sku = models.ForeignKey('ProductSKU', on_delete=models.SET_NULL, null=True, blank=True)
    supplier_po = models.CharField(max_length=100, null=True, blank=True)
    item_ordered = models.CharField(max_length=255, null=True, blank=True)
    received = models.BooleanField(default=False)
    qty = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'products_po'
        ordering = ['-created_at']

    def __str__(self):
        return self.po_ref


class StockControlCode(BaseModel):
    code = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'products_stock_control_code'
        ordering = ['-created_at']

    def __str__(self):
        return self.code


class StockSuppliedTo(BaseModel):
    stock_supplied_to = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'StockSuppliedTos'
        ordering = ['-created_at']
        db_table = 'products_stock_supplied_to'

    def __str__(self):
        return self.stock_supplied_to


class Package(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='packages')
    package_type = models.CharField(max_length=255)

    class Meta:
        db_table = 'products_package'
        ordering = ['-created_at']

    def __str__(self):
        return self.package_type


class CarData(BaseModel):
    marque = models.CharField(max_length=100, blank=True, null=True)
    range = models.CharField(max_length=100, blank=True, null=True)
    from_year = models.IntegerField(blank=True, null=True)
    to_year = models.IntegerField(blank=True, null=True)
    spec_notes = models.TextField(blank=True, null=True)
    tele_mute = models.BooleanField(default=False)
    kram = models.BooleanField(default=False)
    mounting_notes = models.TextField(blank=True, null=True)
    mute_pin = models.CharField(max_length=100, blank=True, null=True)
    vehicle_notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'car_data'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.marque} - {self.range}"

