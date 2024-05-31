from django.db import models
from utilities.models import TimeStamp


class Order(TimeStamp):
    order_ref_number = models.CharField(max_length=100)
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_order')
    customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    current_route = models.TextField(blank=True, null=True)
    engineer = models.ForeignKey('Engineer', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"order created for {self.customer.contact_name} & product {self.product.product_name}"


class KIF(models.Model):
    """The KIF table in your database appears to be a key table for managing order details,
     particularly related to individual items within an order. KIF likely stands for "Key
     Item File" or a similar term that signifies detailed information about items ordered,
      including their pricing, quantities, and status (e.g., returned, credited)"""

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

# class OrderRouteTable(models.Model):
#     order_route = models.CharField(max_length=255, blank=True, null=True)
#     category = models.CharField(max_length=255, blank=True, null=True)
#
#     def __str__(self):
#         return self.order_route

