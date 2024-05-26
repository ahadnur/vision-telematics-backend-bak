from django.db import models


class Order(models.Model):
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_order')
    customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    current_route = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"order created for {self.customer.contact_name} & product {self.product.product_name}"


# class OrderRouteTable(models.Model):
#     order_route = models.CharField(max_length=255, blank=True, null=True)
#     category = models.CharField(max_length=255, blank=True, null=True)
#
#     def __str__(self):
#         return self.order_route


class PO(models.Model):
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

