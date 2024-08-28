from django.db import models
from apps.utilities.models import TimeStamp


class Order(TimeStamp):
    order_ref_number = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    current_route = models.TextField(blank=True, null=True)
    engineer = models.ForeignKey('engineers.Engineer', on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='user_order')
    customer = models.ForeignKey('customers.Customer', related_name='order_customers', on_delete=models.SET_NULL,
                                 null=True, blank=True)

    def __str__(self):
        return f"order created for {self.customer.contact_name}"


# KIF
class OrderItem(models.Model):
    order = models.ForeignKey('orders.Order', related_name='items', on_delete=models.CASCADE, null=True, blank=True)
    product_sku = models.ForeignKey('products.ProductSKU', on_delete=models.CASCADE, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    returned = models.BooleanField(default=False)
    credit_note = models.ForeignKey('customers.Credit', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.quantity} x {self.product_sku.sku_code if self.product_sku.sku_code else ''} for Order {self.order.order_ref_number}"

    def total_price(self):
        total = self.price * self.quantity
        if self.discount:
            total -= self.discount
        return total

    def save(self, *args, **kwargs):
        # Ensure the quantity ordered doesn't exceed available SKU quantity
        if self.quantity > self.product_sku.qty:
            raise ValueError("Ordered quantity exceeds available stock.")
        self.total_price = self.product_sku.unit_price * self.quantity
        super().save(*args, **kwargs)