from django.db import models
from utilities.models import TimeStamp

"""
When the company needs to purchase products or services from suppliers
to fulfill customer orders or maintain inventory, they generate purchase orders.
These purchase orders are recorded in the PO table, which helps track the items
to be procured, their quantities, descriptions, and associated suppliers
"""


class PO(TimeStamp):
    po_ref = models.CharField(max_length=100, unique=True)
    invoice_number = models.ForeignKey('Account', on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()
    description = models.TextField(null=True, blank=True)
    supplier = models.ForeignKey('Supplier', on_delete=models.SET_NULL, null=True, blank=True)
    item_po = models.CharField(max_length=100, null=True, blank=True)
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, blank=True)
    supplier_po = models.CharField(max_length=100, null=True, blank=True)
    item_ordered = models.CharField(max_length=255, null=True, blank=True)
    received = models.BooleanField(default=False)
    qty = models.PositiveIntegerField()

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
