from django.db import models


class PO(models.Model):
    po_ref = models.CharField(max_length=255, null=True, blank=True)
    invoice_number = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    supplier = models.ForeignKey('Supplier', on_delete=models.SET_NULL, null=True, blank=True)
    item_po = models.CharField(max_length=255, null=True, blank=True)
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, blank=True)
    supplier_po = models.CharField(max_length=255, null=True, blank=True)
    item_ordered = models.CharField(max_length=255, null=True, blank=True)
    received = models.BooleanField(default=False)
    qty = models.IntegerField(null=True, blank=True)

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
